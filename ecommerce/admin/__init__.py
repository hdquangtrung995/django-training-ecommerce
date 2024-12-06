from django.contrib import admin
from ecommerce.models import (
    EcomStore,
    EcomCategory,
    EcomProducts,
    EcomProductVariant,
    EcomPromotion,
    EcomPromotionDiscountVariant,
)


from .category import CategoryAdmin
from .products import ProductsAdmin
from .product_variant import ProductVariantAdmin
from .promotion import PromotionAdmin, PromotionDiscountVariantAdmin


class MyEcommerceAdminSite(admin.AdminSite):
    site_header = "My Ecommerce Admin Site"
    site_title = "Ecommerce Admin"
    index_title = "Ecommerce Admin"
    empty_value_display = "N/A"
    site_url = None


my_ecommerce_admin_site = MyEcommerceAdminSite(name="admin")

my_ecommerce_admin_site.register(EcomCategory, CategoryAdmin)
my_ecommerce_admin_site.register(EcomProducts, ProductsAdmin)
my_ecommerce_admin_site.register(EcomProductVariant, ProductVariantAdmin)
my_ecommerce_admin_site.register(EcomPromotion, PromotionAdmin)
my_ecommerce_admin_site.register(
    EcomPromotionDiscountVariant, PromotionDiscountVariantAdmin
)
my_ecommerce_admin_site.register(EcomStore)
