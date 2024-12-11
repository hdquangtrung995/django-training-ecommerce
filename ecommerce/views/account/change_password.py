from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.admin.forms import AdminPasswordChangeForm
from .navigation import navigations


class ChangePassword(FormView):
    login_url = reverse_lazy("ecommerce:login_account")
    template_name = "ecommerce/page/account/change-password.html"
    form_class = AdminPasswordChangeForm
    success_url = reverse_lazy("ecommerce:your_account")

    def get_context_data(self, **kwargs):
        """
        Add your custom context here
        """
        context = super().get_context_data(**kwargs)
        context["account_navigations"] = navigations()
        return context

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        form = AdminPasswordChangeForm(user=self.request.user)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = AdminPasswordChangeForm(user=self.request.user, data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        form.save()
        return HttpResponseRedirect(self.get_success_url())
