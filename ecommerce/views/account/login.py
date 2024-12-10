from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login

from ecommerce.forms import LoginAccountForm


class LoginAccount(FormView):
    template_name = "ecommerce/page/account/login.html"
    form_class = LoginAccountForm
    success_url = reverse_lazy("ecommerce:your_account")

    def get_context_data(self, **kwargs):
        """
        Add your custom context here
        """
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)

        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        user = authenticate(
            self.request,
            username=form.cleaned_data.get("email"),
            password=form.cleaned_data.get("password"),
        )
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return HttpResponseRedirect(reverse("ecommerce:home_page"))
