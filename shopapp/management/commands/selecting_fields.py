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
        self.stdout.write("Start demo select fields")
        users = User.objects.values_list("pk", "username")
        for user in users:
            print(user)
        # products_values = Product.objects.values("pk", "name")
        # for product in products_values:
        #     print(product)
        self.stdout.write(f"Done")
