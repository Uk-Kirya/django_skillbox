from csv import DictReader
from io import TextIOWrapper
import json

from .models import Product, Order


def save_csv_products(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding,
    )

    reader = DictReader(csv_file)
    products = [
        Product(**row)
        for row in reader
    ]
    Product.objects.bulk_create(products)

    return products


def save_csv_orders(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding,
    )

    reader = DictReader(csv_file)

    for row in reader:
        product_ids = json.loads(row['products'])
        user_id = row['user']

        order = Order.objects.create(
            delivery_address=row["delivery_address"],
            promocode=row["promocode"],
            user_id=int(user_id),
        )

        order.products.set(Product.objects.filter(pk__in=product_ids))
