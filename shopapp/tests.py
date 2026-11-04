import time
from string import ascii_letters
from random import choices

from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from .models import Product, Order
from .utils import add_two_numbers


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 5)
        self.assertEqual(result, 7)


class ProductCreateTestCase(TestCase):
    def setUp(self):
        self.product_name = ''.join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_product_create(self):
        response = self.client.post(
            reverse('shopapp:products_create'),
            {
                "name": self.product_name,
                "price": "123.45",
                "description": "Good Product for test",
                "discount": "10",
            }
        )
        self.assertRedirects(response, reverse('shopapp:products_list'))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name='Best Product')

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_get_product_content(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk': self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductsListViewTestCase(TestCase):
    fixtures = [
        'products-fixtures.json',
        'users-fixtures.json',
    ]

    def test_products(self):
        response = self.client.get(reverse('shopapp:products_list'))
        self.assertQuerySetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context['products']),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, 'shopapp/products.html')


class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='Bob', password='qwerty')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_orders_list(self):
        response = self.client.get(reverse('shopapp:orders_list'))
        self.assertContains(response, 'Orders')

    def test_redirect_order(self):
        self.client.logout()
        response = self.client.get(reverse('shopapp:orders_list'))
        self.assertIn(str(settings.LOGIN_URL), response.url)


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        permissions = Permission.objects.get(codename='view_order')
        cls.user = User.objects.create_user(username='test_bob', password='qwerty')
        cls.user.user_permissions.add(permissions)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.product_1 = Product.objects.create(name='Product 1', price='123', created_by=self.user)
        self.product_2 = Product.objects.create(name='Product 2', price='321', created_by=self.user)
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            delivery_address='г.Сочи, ул.Магнитогорская 23/47',
            promocode='salesale',
            created_at=time.time(),
            user=self.user
        )
        self.order.products.set([self.product_1, self.product_2])

    def tearDown(self):
        self.product_1.delete()
        self.product_2.delete()
        self.client.logout()
        self.order.delete()

    def test_order(self):
        response = self.client.get(reverse('shopapp:order_details', args=[self.order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'г.Сочи, ул.Магнитогорская 23/47')
        self.assertContains(response, 'salesale')

        orders = self.client.get(reverse('shopapp:orders_list'))
        self.assertQuerySetEqual(
            qs=Order.objects.all(),
            values=(o.pk for o in orders.context['order_list']),
            transform=lambda o: o.pk
        )


class OrdersExportTestCase(TestCase):
    fixtures = [
        'orders-fixtures.json',
        'products-fixtures.json',
        'users-fixtures.json',
    ]

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='bob', password='qwerty', is_staff=True)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def tearDown(self):
        self.client.logout()

    def test_export(self):
        response = self.client.get(reverse('shopapp:export'))
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by('pk').all()
        expected_data = [
            {
                'id': order.pk,
                'location': order.delivery_address,
                'promocode': order.promocode,
                'user': order.user,
                'products': [
                    {
                        'id': product.pk
                    }
                    for product in order.products.all()
                ]
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(
            orders_data['orders'],
            expected_data,
        )

