from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from ecommerce.forms import AccountChangeWithOutPasswordForm
from user.models import EcomUser
from wrapper import query_debugger
from .navigation import navigations


class YourAccount(LoginRequiredMixin, FormView):
    login_url = reverse_lazy("ecommerce:login_account")
    template_name = "ecommerce/page/account/index.html"
    form_class = AccountChangeWithOutPasswordForm
    success_url = reverse_lazy("ecommerce:your_account")

    def get_context_data(self, **kwargs):
        """
        Add your custom context here
        """
        context = super().get_context_data(**kwargs)
        context["account_navigations"] = navigations()
        return context

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

    def post(self, request, *args, **kwargs):
        instance = get_object_or_404(EcomUser, id=request.user.id)
        form = AccountChangeWithOutPasswordForm(request.POST, instance=instance)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        form.save()
        return super().form_valid(form)
