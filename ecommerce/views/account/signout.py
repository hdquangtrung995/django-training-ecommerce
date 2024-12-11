from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse


def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse("ecommerce:home_page"))
