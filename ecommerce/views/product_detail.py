from django.http import Http404
from django.views.generic.detail import DetailView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from ecommerce.models import EcomProducts
from ecommerce.serializers import ProductWithCategorySerializer

policies = [
    {
        "src": "https://file.hstatic.net/1000253775/file/z4635451118875_c98fff6e965c4957a2beef70df6df0f8_afcea78391a640c9bcef22ce88aca7d6.jpg",
        "label": "Đổi trả tận nhà trong  vòng 15 ngày",
    },
    {
        "src": "https://file.hstatic.net/1000253775/file/z4635451151763_13f64ed25050f361cfb0a70fda62b2c2_efbb28df6328412b9200cd92a795396e.jpg",
        "label": "Miễn phí vận chuyển  đơn từ 399k",
    },
    {
        "src": "https://file.hstatic.net/1000253775/file/z4635451129757_228e4824d8a593038b9f20d5e53d4d08_7e46b4c108bc481e8c2351f909bdcba4.jpg",
        "label": "Bảo hành trong vòng 30 ngày",
    },
    {
        "src": "https://file.hstatic.net/1000253775/file/z4635451140541_2b09e178f1b8b4763b266875fd2c8db6_8b536c9ae5e24c17961fdb906d3f5022.jpg",
        "label": "Hotline  0287.100.6789 hỗ trợ từ 8h30-24h",
    },
    {
        "src": "https://file.hstatic.net/1000253775/file/z4635451129712_78e0e70db6fffe43fbb9a3e680cb3ed0_a2b8379adf4843a4898c621b37c2b42a.jpg",
        "label": "Giao hàng toàn quốc",
    },
    {
        "src": "https://file.hstatic.net/1000253775/file/z4635451151761_2fe8731e9d20060a54130996be16cd2e_e8e090599dd9467abdd66feb9ba3474f.jpg",
        "label": "Có cộng dồn. Ưu đãi KHTT",
    },
]


class ProductDetail(DetailView):
    model = EcomProducts
    context_object_name = "product_detail"
    template_name = "ecommerce/page/detail_product/index.html"
    queryset = EcomProducts.active.all()

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        queryset = self.get_queryset()
        slug = self.kwargs.get(self.slug_url_kwarg)
        if slug is not None:
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug}).select_related("category")

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
            return obj
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            if self.object:
                context["object"] = self.object
                data = ProductWithCategorySerializer(self.object)
                context[self.context_object_name] = data.data

            context["policies"] = policies
            context["breadcrumbs"] = [
                {"href": reverse("ecommerce:home_page"), "label": "home"},
                {"href": reverse("ecommerce:product_page"), "label": "all products"},
                {"href": "#", "label": self.kwargs.get(self.slug_url_kwarg)},
            ]
        except Exception as error:
            print("__name__: ", __name__, error)
            context["error"] = f"An unexpected error occurred: {str(error)}"
        return context
