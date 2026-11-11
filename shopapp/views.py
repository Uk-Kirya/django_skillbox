import logging
from csv import DictWriter

from django.core.cache import cache
from django.contrib.auth.models import Group, User
from django.contrib.syndication.views import Feed
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django_filters.rest_framework import DjangoFilterBackend

from .common import save_csv_products
from .forms import ProductForm, OrderForm, GroupForm
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter

from drf_spectacular.utils import extend_schema, OpenApiResponse

log = logging.getLogger(__name__)


@extend_schema(
    description='Product views CRUD'
)
class ProductViewSet(ModelViewSet):
    """
    Предоставление товаров, а также, полный CRUD
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('name', 'price', 'description', 'discount')
    ordering_fields = ('price', 'created_at')
    filterset_fields = ('name', 'price', 'archived')

    @extend_schema(
        summary='Get one Product by ID',
        description='Retrieves **Product** by ID or 404',
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description='Product not found'),
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @action(methods=['get'], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type="text/csv")
        filename = "products-export.csv"
        response["Content-Desposition"] = f"attachment; filename={filename}"

        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            'name', 'price', 'description', 'discount'
        ]
        queryset = queryset.only(*fields)

        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })

        return response

    @action(methods=['post'], detail=False, parser_classes=[MultiPartParser])
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES['file'].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)



class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('delivery_address', 'promocode', 'user', 'products')
    ordering_fields = ('created_at',)
    filterset_fields = ('created_at', 'promocode')



class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Apple', 29),
            ('Orange', 40),
            ('Potato', 51)
        ]
        context = {
            "products": products,
        }
        log.debug("Products for shop Index: %s", products)
        log.info("Rendering shop Index: %s", products)
        return render(request, 'shopapp/index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related("permissions").all(),
            "orders": Order.objects.all(),
        }
        return render(request, 'shopapp/groups.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class ProductsListView(ListView):
    template_name = 'shopapp/products.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)


class ProductDetailsView(DetailView):
    template_name = 'shopapp/product-detail.html'
    model = Product
    context_object_name = 'product'


class ProductCreateView(CreateView):
    # def test_func(self):
    #     return self.request.user.is_superuser

    model = Product
    fields = "name", "price", "description", "discount"
    template_name = 'shopapp/product-form.html'
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    fields = "name", "price", "description", "discount"
    template_name = 'shopapp/product-update-form.html'

    def get_success_url(self):
        return reverse("shopapp:product_details", kwargs={"pk": self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')
    template_name = 'shopapp/product-confirm-delete.html'

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save(update_fields=['archived'])
        return HttpResponseRedirect(success_url)


def create_product(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse("shopapp:products_list")
            return redirect(url)
    else:
        form = ProductForm()

    context = {
        "form": form,
    }
    return render(request, 'shopapp/create-product.html', context=context)


def orders_list(request: HttpRequest):
    context = {
        "orders": Order.objects.select_related("user").prefetch_related("products").all(),
    }
    return render(request, 'shopapp/orders.html', context=context)


class OrdersList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'shopapp.view_order'
    template_name = 'shopapp/orders.html'

    def get_queryset(self):
        return Order.objects.select_related("user").prefetch_related("products").filter(user=self.request.user)


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    template_name = 'shopapp/order-detail.html'
    queryset = Order.objects.select_related("user").prefetch_related("products")


def create_order(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            url = reverse("shopapp:orders_list")
            return redirect(url)
    else:
        form = OrderForm()

    context = {
        "form": form,
    }
    return render(request, "shopapp/create-order.html", context=context)


class ExportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by('pk').all()
        orders_data = [
            {
                'id': order.pk,
                'location': order.delivery_address,
                'promocode': order.promocode,
                'user': order.user.username,
                'products': [
                    {
                        'id': product.pk,
                    }
                    for product in order.products.all()
                ]
            }
            for order in orders
        ]
        return JsonResponse({'orders': orders_data})


class LatestProductsFeed(Feed):
    title = "Новинки"
    description = "Тут последние, добавленные товары"
    link = reverse_lazy("shopapp:products_list")

    def items(self):
        return Product.objects.filter(archived=False).order_by('-created_at').all()[:3]


class UserOrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shopapp/user_orders_list.html'
    context_object_name = 'order_list'

    def get_queryset(self):
        self.owner = get_object_or_404(User, pk=self.kwargs.get('user_id'))
        return Order.objects.filter(user=self.owner).prefetch_related("products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        return context


class UserOrdersExportView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        owner = get_object_or_404(User, pk=user_id)
        cache_key = f"owner_{owner.pk}"

        orders = cache.get(cache_key)
        if orders is None:
            orders = Order.objects.filter(user=owner).prefetch_related("products").order_by('pk')
        else:
            cache.set(cache_key, orders, 300)

        serializer = OrderSerializer(orders, many=True)
        return JsonResponse(serializer.data, safe=False)