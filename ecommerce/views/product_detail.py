from django.views.generic.detail import DetailView

from ecommerce.models import EcomProducts, EcomProductVariant


class ProductDetail(DetailView):
    model = EcomProducts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
