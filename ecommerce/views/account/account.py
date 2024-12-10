from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.functional import SimpleLazyObject

from ecommerce.forms import AccountChangeWithOutPasswordForm
from user.models import EcomUser
from wrapper import query_debugger


class YourAccount(LoginRequiredMixin, FormView):
    login_url = reverse_lazy("ecommerce:login_account")
    template_name = "ecommerce/page/account/index.html"
    form_class = AccountChangeWithOutPasswordForm
    # success_url = reverse_lazy("ecommerce:product_page")
    # initial = EcomUser.objects.get(pk="5dca48dd-fc31-4c42-8fa1-0e69d2687ad7").values()

    def get_context_data(self, **kwargs):
        """
        Add your custom context here
        """
        context = super().get_context_data(**kwargs)
        return context

    @query_debugger
    def get_initial(self):
        initial_data = {
            "email": self.request.user.email,
            "first_name": self.request.user.first_name,
            "last_name": self.request.user.last_name,
            "phone": self.request.user.phone,
            "email_verified": self.request.user.email_verified,
            "date_of_birth": self.request.user.date_of_birth,
        }
        return initial_data

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        return self.render_to_response(self.get_context_data())
