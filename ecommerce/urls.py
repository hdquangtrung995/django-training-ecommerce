from django.urls import path
from ecommerce.views import (
    HomeView,
    AllProductsWithFilter,
    ProductDetail,
    RegisterAccount,
    YourAccount,
    LoginAccount,
    ChangePassword,
    sign_out,
    CustomerCart,
    GhnJsonView,
)

app_name = "ecommerce"
urlpatterns = [
    path("", HomeView.as_view(), name="home_page"),
    path("products/", AllProductsWithFilter.as_view(), name="product_page"),
    path("products/<slug:slug>", ProductDetail.as_view(), name="product_detail"),
    path("cart/", CustomerCart.as_view(), name="your_cart"),
    path("delivery/fee/", GhnJsonView.as_view(), name="signout_account"),
    path("account/", YourAccount.as_view(), name="your_account"),
    path("account/register/", RegisterAccount.as_view(), name="register_account"),
    path("account/login/", LoginAccount.as_view(), name="login_account"),
    path(
        "account/change/password",
        ChangePassword.as_view(),
        name="change_password_account",
    ),
    path("account/signout/", sign_out, name="signout_account"),
]
