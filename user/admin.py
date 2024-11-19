from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import EcomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomEcomUserCreationForm(UserCreationForm):
    """
    Specify the user model created while adding a user
    on the admin page.
    """

    class Meta:
        model = EcomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "date_of_birth",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        ]


class CustomEcomUserChangeForm(UserChangeForm):
    """
    Specify the user model edited while editing a user on the
    admin page.
    """

    class Meta:
        model = EcomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "date_of_birth",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        ]


class CustomEcomUserAdmin(UserAdmin):
    add_form = CustomEcomUserCreationForm
    form = CustomEcomUserChangeForm

    model = EcomUser
    list_display = (
        "email",
        "first_name",
        "last_name",
        "date_of_birth",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "first_name",
        "last_name",
        "date_of_birth",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password",
                    "date_of_birth",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                    "date_of_birth",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


# Register your models here.
admin.site.register(EcomUser, CustomEcomUserAdmin)
