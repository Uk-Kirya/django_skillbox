from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    ShopIndexView,
    GroupsListView,
    ProductsListView,
    OrdersList,
    ProductCreateView,
    create_order,
    ProductDetailsView,
    OrderDetailView,
    ProductUpdateView,
    ProductDeleteView,
    ExportView,

    ProductViewSet,
    OrderViewSet,
    LatestProductsFeed
)

app_name = "shopapp"

routers = DefaultRouter()
routers.register('products', ProductViewSet)
routers.register('orders', OrderViewSet)

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("api/", include(routers.urls)),
    path("groups/", GroupsListView.as_view(), name="groups_list"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/latest/feed/", LatestProductsFeed(), name="product__feed"),
    path("products/create/", ProductCreateView.as_view(), name="products_create"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name="product_delete"),
    path("orders/", OrdersList.as_view(), name="orders_list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_details"),
    path("orders/create/", create_order, name="create_order"),
    path('export/', ExportView.as_view(), name='export'),
]