from django.contrib import admin
from ecommerce.models import EcomPromotionDiscountVariant, EcomProductPromotionExtra
from ecommerce.forms import PromotionChangeForm


class PromotionDiscountVariantInlineAdmin(admin.TabularInline):
    model = EcomPromotionDiscountVariant
    extra = 1


class ProductPromotionExtraInlineAdmin(admin.TabularInline):
    model = EcomProductPromotionExtra
    extra = 1


class PromotionAdmin(admin.ModelAdmin):
    form = PromotionChangeForm
    fields = [
        "id",
        "name",
        "description",
        "link_to",
        "thumbnail",
        "promotion_type",
        "code",
        "start_date",
        "end_date",
        "is_active",
        "can_stack",
    ]
    readonly_fields = ["id"]
    list_display = ["id", "name", "code", "promotion_type", "start_date", "end_date"]
    list_display_links = ["id"]
    list_editable = ["name", "code", "start_date", "end_date"]
    list_filter = ["promotion_type"]
    search_fields = ["name", "promotion_type"]
    show_facets = admin.ModelAdmin.show_facets.ALWAYS
    inlines = [PromotionDiscountVariantInlineAdmin, ProductPromotionExtraInlineAdmin]


class PromotionDiscountVariantAdmin(admin.ModelAdmin):
    fields = [
        "id",
        "min_purchase",
        "max_purchase",
        "min_item",
        "max_item",
        "min_discount",
        "max_discount",
        "discount_type",
        "discount_value",
        "promotion",
    ]
    readonly_fields = ["id"]
    list_display = ["id", "promotion__name", "discount_type", "discount_value"]
    list_display_links = ["id", "promotion__name"]
    list_editable = ["discount_type", "discount_value"]
    list_filter = ["discount_type", "discount_value"]
    search_fields = ["discount_type"]
