from decimal import Decimal

from django.conf import settings
from rest_framework import serializers
from ecommerce.models import (
    EcomProducts,
    EcomProductVariant,
    EcomPromotion,
    EcomPromotionDiscountVariant,
)
from ecommerce.helpers import find
from ecommerce.serializers.promotions import (
    PromotionDiscountVariantSerializer,
    # PromotionThroughSerializer,
    BasePromotionSerializer,
    PromotionExculdeProductSerializer,
)
from ecommerce.serializers.dynamic import DynamicFieldsModelSerializer


class ProductsVariantSerializer(DynamicFieldsModelSerializer):
    size = serializers.SerializerMethodField()

    class Meta:
        model = EcomProductVariant
        fields = "__all__"
        # fields = [
        #     "size",
        #     "color",
        #     "sku",
        #     "stock",
        #     "price",
        #     "gender",
        #     "product_id",
        # ]

    def get_size(self, obj):
        value, label = find(
            lambda item: item[1]
            if item[0] == obj.size
            else {"value": None, "label": None},
            list(EcomProductVariant.SIZES),
        )
        return {"value": value, "label": label}


# class BaseProductsSerializer(DynamicFieldsModelSerializer):
#     variants = ProductsVariantSerializer(many=True)
#     promotions = BasePromotionSerializer(
#         source="ecomproductpromotionextra_set", many=True
#     )

#     class Meta:
#         model = EcomProducts
#         fields = "__all__"
# fields = [
#     "id",
#     "name",
#     "description",
#     "product_code",
#     "slug",
#     "thumbnail",
#     "is_active",
#     "galleries",
#     "variants",
#     "created",
#     "modified",
#     "promotions",
# ]


# class ProductsPriceSerializer(DynamicFieldsModelSerializer):
#     price = serializers.SerializerMethodField()
#     promotions = PromotionThroughSerializer(
#         source="ecomproductpromotionextra_set", many=True
#     )

#     class Meta:
#         model = EcomProducts
#         fields = ["id", "name", "slug", "thumbnail", "price", "promotions"]

#     def get_price(self, obj):
#         get_all_variants = obj.variants.all()
#         variants = ProductsVariantSerializer(get_all_variants, many=True).data
#         first_item = find(lambda item: item.get("price"), variants)
#         return first_item.get("price") if first_item else None


# class ProductsNewEverydaySerializer(ProductsPriceSerializer):
#     promotions = serializers.SerializerMethodField()

#     class Meta:
#         model = EcomProducts
#         fields = ["id", "name", "slug", "thumbnail", "price", "promotions"]

#     def get_promotions(self, obj):
#         promotions = PromotionExculdeProductSerializer(obj.promotions, many=True)
#         target_promotion = find(
#             lambda item: item.get("promotion_type")
#             in [
#                 EcomPromotion.PROMOTION_TYPE.flashsale,
#                 EcomPromotion.PROMOTION_TYPE.product,
#             ],
#             promotions.data,
#         )
#         return target_promotion
