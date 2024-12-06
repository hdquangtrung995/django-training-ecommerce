from django.contrib import admin
from ecommerce.models import (
    EcomProductVariant,
    EcomPromotion,
    EcomProductPromotionExtra,
)


class ProductVariantInlineAdmin(admin.TabularInline):
    model = EcomProductVariant
    extra = 1


class ProductPromotionInlineAdmin(admin.TabularInline):
    model = EcomProductPromotionExtra
    extra = 1
    autocomplete_fields = ["promotion"]


class ProductsAdmin(admin.ModelAdmin):
    fields = [
        "id",
        "name",
        "description",
        "product_code",
        "thumbnail",
        "is_active",
        "galleries",
        "category",
        "slug",
        # "promotions",
    ]
    readonly_fields = ["id"]

    list_display = ["id", "name", "category", "slug"]
    list_display_links = ["id"]
    list_editable = ["name"]
    list_filter = ["category", "promotions"]
    list_select_related = ["category"]

    prepopulated_fields = {"slug": ["name"]}
    show_facets = admin.ModelAdmin.show_facets.ALWAYS
    search_fields = ["name", "id"]
    inlines = [ProductVariantInlineAdmin, ProductPromotionInlineAdmin]
