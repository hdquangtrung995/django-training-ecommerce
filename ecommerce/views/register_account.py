from django.views.generic.edit import FormView
from ecommerce.forms import RegisterAccountForm


class RegisterAccount(FormView):
    template_name = "ecommerce/page/account/register.html"
    form_class = RegisterAccountForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        """
        Add your custom context here
        """
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
