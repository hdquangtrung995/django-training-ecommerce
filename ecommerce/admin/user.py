from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from ecommerce.forms import AccountCreationForm, AccountChangeForm


class UserAdmin(BaseUserAdmin):
    form = AccountChangeForm
    add_form = AccountCreationForm

    ordering = ("email",)
    readonly_fields = ["id"]
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("first_name", "last_name", "email")
    fieldsets = (
        (None, {"fields": ("id", "email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "email_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined", "date_of_birth")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "phone",
                    "email",
                    "password1",
                    "password2",
                    "date_of_birth",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "email_verified",
                ),
            },
        ),
    )
