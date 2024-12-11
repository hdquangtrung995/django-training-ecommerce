from django.urls import reverse


def navigations():
    return [
        {
            "name": "profile",
            "href": reverse("ecommerce:your_account"),
            "icon": "fa-user",
        },
        {
            "name": "change password",
            "href": reverse("ecommerce:change_password_account"),
            "icon": "fa-lock",
        },
    ]
