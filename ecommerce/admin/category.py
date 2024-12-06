from django.contrib import admin


# @admin.register(EcomCategory)
class CategoryAdmin(admin.ModelAdmin):
    fields = ["id", "name", "display_name", "name_slug", "parent"]
    readonly_fields = ["id", "name_slug"]

    list_display = ["id", "name", "display_name", "parent"]
    list_display_links = ["id", "name"]
    list_editable = ["display_name"]
    list_filter = ["name"]

    show_facets = admin.ModelAdmin.show_facets.ALWAYS
