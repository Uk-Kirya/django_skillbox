from django import forms
from django.contrib.auth.models import Group
from django.forms import ModelForm

from .models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount"


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "products", "delivery_address", "promocode"


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ["name"]


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()


class CSVImportOrdersForm(forms.Form):
    csv_file = forms.FileField()