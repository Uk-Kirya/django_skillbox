from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Product

from django.db import transaction


class Command(BaseCommand):
    """
    Create Order
    """

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Start demo bulk actions")

        result = Product.objects.filter(
            name__contains="SmartPhone"
        ).update(discount=10)

        print(result)

        # info = [
        #     ('SmartPhone 1', 199, 2),
        #     ('SmartPhone 2', 299, 2),
        #     ('SmartPhone 3', 399, 2),
        # ]
        #
        # products = [
        #     Product(name=name, price=price, created_by_id=author)
        #     for name, price, author in info
        # ]
        #
        # result = Product.objects.bulk_create(products)
        #
        # for obj in result:
        #     print(obj)

        self.stdout.write(f"Done")
