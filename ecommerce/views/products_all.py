from django.views.generic import ListView

from ecommerce.models import EcomProducts


class AllProductsWithFilter(ListView):
    model = EcomProducts
    context_object_name = "products"
    template_name = "ecommerce/page/all_products/index.html"

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
