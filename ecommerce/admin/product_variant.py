from django.contrib import admin


class ProductVariantAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "id",
                    "sku",
                    "stock",
                    "price",
                    ("gender", "size"),
                    "product",
                ],
            },
        ),
        (
            "Color",
            {
                "fields": [("color", "color_hex")],
            },
        ),
    ]

    list_display = ["id", "product__name", "price", "stock", "color"]
    list_display_links = ["id"]
    list_editable = ["price", "stock", "color"]
    list_filter = ["color", "size"]
    list_select_related = True
    show_facets = admin.ModelAdmin.show_facets.ALWAYS

    # radio_fields = {"size": admin.HORIZONTAL, "gender": admin.HORIZONTAL}

    autocomplete_fields = [
        "product"
    ]  # Pick either autocomplete_fields or raw_id_fields
    # raw_id_fields = ["product"]
