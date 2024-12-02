from django.urls import path
from ecommerce.views import HomeView, AllProductsWithFilter, ProductDetail

app_name = "ecommerce"
urlpatterns = [
    path("", HomeView.as_view(), name="home_page"),
    path("products/", AllProductsWithFilter.as_view(), name="product_page"),
    path("products/<slug:slug>", ProductDetail.as_view(), name="product_detail"),
]
