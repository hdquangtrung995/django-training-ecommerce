import json
import uuid
from itertools import chain

from functools import reduce
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from django.db.models import Prefetch
from rest_framework.renderers import JSONRenderer

from ecommerce.models import EcomProducts, EcomPromotion, EcomProductVariant
from ecommerce.serializers import BaseProductsSerializer, BasePromotionSerializer
from ecommerce.helpers import find, find_index
from ecommerce.forms import DeliveryFeeForm
from services.giao_hang_nhanh import GhnApiService
from wrapper import query_debugger
from services.promotion import PromotionsDiscountHandler


class CustomerCart(TemplateView):
    template_name = "ecommerce/page/cart/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        as_coupon_promotions = EcomPromotion.active.filter(
            promotion_type__in=[
                EcomPromotion.PROMOTION_TYPE.coupon,
                EcomPromotion.PROMOTION_TYPE.freeship,
            ]
        ).prefetch_related("discount_variant")
        context["coupon_promotions"] = (
            JSONRenderer()
            .render(BasePromotionSerializer(as_coupon_promotions, many=True).data)
            .decode("utf-8")
        )

        form = DeliveryFeeForm()
        context["form"] = form

        return context

    def handlePromotionCoupon(self, cart_items, promotions):
        cart_items = json.loads(cart_items)
        promotions_dict = json.loads(promotions)
        variants_id_tuple = [
            (
                uuid.UUID(key.split(".")[0]),
                int(value.get("variantId")),
                int(value.get("quantity")),
            )
            for key, value in cart_items.items()
        ]
        # Return list of product's id, variant's id and exclude quantity number
        ids = [item for sublist in variants_id_tuple for item in sublist[:2]]

        promotions_prefetched = Prefetch(
            "promotions",
            queryset=EcomPromotion.active.prefetch_related("discount_variant"),
        )
        product_variants_prefetched = Prefetch(
            "variants", queryset=EcomProductVariant.objects.filter(id__in=ids)
        )

        products_lookup = EcomProducts.active.filter(
            id__in=ids, variants__id__in=ids
        ).prefetch_related(product_variants_prefetched, promotions_prefetched)

        for product in products_lookup:
            # Create a dictionary for quick lookup of variants by ID
            variants_by_id = {variant.id: variant for variant in product.variants.all()}

            # Iterate through the list of tuples and find matching product_id
            for index, (product_id, variant_id, quantity) in enumerate(
                variants_id_tuple
            ):
                if product.id == product_id:  # Check for product_id match
                    existing_variant = variants_by_id.get(
                        variant_id
                    )  # Look up the variant
                    if existing_variant:
                        # Remove the processed entry and update the variant
                        variants_id_tuple.pop(index)
                        existing_variant.quantity = quantity
                        product.selected_variant = existing_variant
                        break  # Exit loop once a match is found

        promotion_handler = PromotionsDiscountHandler(promotions_dict, products_lookup)
        return [
            *promotion_handler.delivery_promotions(),
            *promotion_handler.validate_coupon_promotions_based_on_order(),
        ]

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        query_parameters = request.GET

        if cart_items := query_parameters.get("contextonly"):
            promotions = self.handlePromotionCoupon(
                cart_items, context["coupon_promotions"]
            )
            return JsonResponse(promotions, safe=False)

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        products = dict()

        for key, value in body.items():
            pid = key.split(".")[0]
            if products.get(pid):
                products = {
                    **products,
                    pid: [*products[pid], {**value, "id": pid}],
                }
            else:
                products = {
                    **products,
                    pid: [
                        {
                            **value,
                            "id": pid,
                        }
                    ],
                }

        flatten_data = list(chain.from_iterable(products.values()))

        promotions_prefetched = Prefetch(
            "promotions",
            queryset=EcomPromotion.active.prefetch_related("discount_variant").all(),
        )
        products_lookup = EcomProducts.active.filter(
            id__in=products.keys()
        ).prefetch_related("variants", promotions_prefetched)
        data_serialized = BaseProductsSerializer(
            products_lookup, many=True, exclude=["galleries"]
        )
        products_grouping = reduce(
            lambda acc, curr: {**acc, curr.get("id"): curr}, data_serialized.data, {}
        )

        def cb(acc, curr):
            if (
                (product := products_grouping.get(curr.get("id")))
                and (
                    targetVariant := find(
                        lambda item: item.get("id") == curr.get("variantId"),
                        product.get("variants"),
                    )
                )
                and (quantity := curr.get("quantity"))
            ):
                acc.append(
                    {
                        **product,
                        "selectedVariant": {**targetVariant, "quantity": quantity},
                    }
                )
                return acc
            return acc

        response = reduce(cb, flatten_data, [])
        return JsonResponse(response, safe=False)
