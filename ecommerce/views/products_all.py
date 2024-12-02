from django.views.generic import ListView
from django.db.models import Count

from ecommerce.models import EcomProducts, EcomProductVariant
from ecommerce.serializers import (
    BaseProductsSerializer,
)
from ecommerce.core.utils.discount_detail import discount_detail


class AllProductsWithFilter(ListView):
    model = EcomProducts
    context_object_name = "products"
    template_name = "ecommerce/page/all_products/index.html"
    paginate_by = 20
    ordering = ["-created"]
    queryset = EcomProducts.objects.filter(is_active=True)
    page_kwarg = "page"

    def get_queryset(self):
        queryset = self.queryset.prefetch_related(
            "variants", "promotions", "promotions__discount_variant"
        )
        ordering = self.get_ordering()

        for key, value in self.request.GET.items():
            if key == "category":
                queryset = queryset.filter(category__name_slug__in=value.split(","))
            if key == "size":
                queryset = queryset.filter(variants__size__in=value.split(","))
            if key == "color":
                queryset = queryset.filter(variants__color__in=value.lower().split(","))

        queryset = queryset.distinct().order_by(*ordering)
        return queryset

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            queryset = self.object_list
            page_size = self.get_paginate_by(queryset)

            if page_size:
                paginator, page, queryset, is_paginated = self.paginate_queryset(
                    queryset, page_size
                )
                elided_page_range = paginator.get_elided_page_range(
                    page.number, on_each_side=2, on_ends=1
                )
                context = {
                    "paginator": paginator,
                    "page_obj": page,
                    "is_paginated": is_paginated,
                    "object_list": queryset,
                    "elided_page_range": elided_page_range,
                }
            else:
                context = {
                    "paginator": None,
                    "page_obj": None,
                    "is_paginated": False,
                    "object_list": queryset,
                }

            all_products_serializer = BaseProductsSerializer(
                queryset, many=True, exclude=["galleries"]
            )
            all_products = map(discount_detail, all_products_serializer.data)
            color_lookup = (
                EcomProductVariant.objects.values("color")
                .annotate(num=Count("color"))
                .order_by("color")
            )
            colors = [i["color"] for i in color_lookup]

            context["sizes"] = EcomProductVariant.SIZES
            context["colors"] = colors
            context[self.context_object_name] = all_products
            return context
        except Exception as error:
            print("ERROR: ", error)
