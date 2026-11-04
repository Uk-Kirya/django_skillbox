from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path

from shopapp.models import Product, Order
from .admin_mixins import ExportCSVMixin
from .common import save_csv_products, save_csv_orders
from .forms import CSVImportForm, CSVImportOrdersForm


class ProductInline(admin.TabularInline):
    model = Product.orders.through


@admin.action(description="Archive products")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description="Unarchive products")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.action(description="Insale products")
def mark_insale(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(availability=True)


@admin.action(description="Outsale products")
def mark_outsale(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(availability=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportCSVMixin):
    change_list_template = "shopapp/products_changelist.html"
    actions = [
        mark_archived,
        mark_unarchived,
        mark_insale,
        mark_outsale,
        "export_csv"
    ]
    inlines = [
        ProductInline,
    ]
    list_display = "pk", "name", "description_short", "price", "discount", "archived", "availability"
    list_display_links = "pk", "name"
    ordering = "pk",
    search_fields = "name", "description",

    fieldsets = [
        (None, {
            "fields": ("name", "description"),
        }),
        ("Price options", {
            "fields": ("price", "discount"),
        }),
        ("Extra options", {
            "fields": ("archived", "availability"),
            "classes": ("collapse",)
        })
    ]

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {"form": form}
            return render(request, 'admin/csv_form.html', context)
        form = CSVImportForm(request.POST, request.FILES)

        if not form.is_valid():
            context = {"form": form}
            return render(request, 'admin/csv_form.html', context, status=400)

        save_csv_products(
            file=form.files["csv_file"].file,
            encoding=request.encoding,
        )

        self.message_user(request, "Successfully imported products", level=messages.SUCCESS)

        return redirect('..')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-products-csv/",
                self.import_csv,
                name="import_products_csv",
            ),
        ]
        return new_urls + urls


class ProductInline(admin.TabularInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = "shopapp/orders_changelist.html"
    inlines = [
        ProductInline,
    ]
    list_display = "delivery_address", "promocode", "created_at", "user_verbose"

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportOrdersForm()
            context = {"form": form}
            return render(request, 'admin/csv_form.html', context)
        form = CSVImportOrdersForm(request.POST, request.FILES)

        if not form.is_valid():
            context = {"form": form}
            return render(request, 'admin/csv_form.html', context, status=400)

        save_csv_orders(
            file=form.files["csv_file"].file,
            encoding=request.encoding,
        )

        self.message_user(request, "Successfully imported orders", level=messages.SUCCESS)

        return redirect('..')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-orders-csv/",
                self.import_csv,
                name="import_orders_csv",
            ),
        ]
        return new_urls + urls
