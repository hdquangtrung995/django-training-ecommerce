from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404

from django.utils.text import slugify

from ecommerce.helpers import generate_sku
from ecommerce.models import EcomStoreBranch, EcomStore, EcomProductVariant
from ecommerce.serializers import ProductsSerializer, ProductsVariantSerializer
from ecommerce.models import EcomProducts, EcomStore, EcomProductVariant, EcomCategory
from ecommerce.serializers import CategorySerializer, StoreSerializer


# Create your views here.
class HomeView(TemplateView):
    template_name = "ecommerce/home.html"

    def get(self, request, *args, **kwargs):
        # return HttpResponse(reverse("ecommerce:home_page"))
        try:
            store = get_object_or_404(EcomStore, pk=1)
            storeSerialized = StoreSerializer(store)

            # for shirt in shirts:
            #     # print("shirt: ", shirt)
            #     vari = EcomProductVariant(
            #         size=EcomProductVariant.SIZES.s,
            #         color="black",
            #         sku=generate_sku(prefix="SKU"),
            #         stock=3,
            #         price=300000.00,
            #         gender=EcomProductVariant.GENDER.male,
            #         product_id=shirt,
            #     )
            #     empty.append(vari)

            # product = EcomProducts.objects.prefetch_related("variants").get(
            #     pk="0aef564b-6132-41c6-81c5-ef1f0d27dc45"
            # )
            # print("product: ", ProductsSerializer(product).data)

            vari = EcomProductVariant.objects.get(pk=3)
            print("data: ", ProductsVariantSerializer(vari).data)

            return HttpResponse(
                render(
                    request,
                    self.template_name,
                    {"list_banners": storeSerialized.data.get("banners", [])},
                )
            )
        except Exception as e:
            print("error: ", e)
            return 404
