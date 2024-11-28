from rest_framework import serializers

from ecommerce.helpers import find
from ecommerce.models import (
    EcomPromotion,
    EcomPromotionDiscountVariant,
    EcomProductPromotionExtra,
)
from ecommerce.serializers.dynamic import DynamicFieldsModelSerializer


class PromotionDiscountVariantSerializer(DynamicFieldsModelSerializer):
    discount_type = serializers.SerializerMethodField()

    class Meta:
        model = EcomPromotionDiscountVariant
        fields = "__all__"
        # fields = [
        #     "min_purchase",
        #     "max_purchase",
        #     "min_item",
        #     "max_item",
        #     "min_discount",
        #     "max_discount",
        #     "discount_type",
        #     "discount_value",
        # ]

    def get_discount_type(self, obj):
        value, label = find(
            lambda item: item[1]
            if item[0] == obj.discount_type
            else {"value": None, "label": None},
            list(EcomPromotionDiscountVariant.DISCOUNT_TYPE),
        )
        return {"value": value, "label": label}


class BasePromotionSerializer(DynamicFieldsModelSerializer):
    discount_variant = PromotionDiscountVariantSerializer()
    promotion_type = serializers.SerializerMethodField()

    class Meta:
        model = EcomPromotion
        fields = "__all__"
        # fields = [
        #     "name",
        #     "description",
        #     "link_to",
        #     "thumbnail",
        #     "promotion_type",
        #     "code",
        #     "start_date",
        #     "end_date",
        #     "is_active",
        #     "can_stack",
        #     "discount_variant",
        #     "products",
        # ]

    def get_promotion_type(self, obj):
        promotion_type, label = find(
            lambda item: item[1] if item[0] == obj.promotion_type else None,
            list(EcomPromotion.PROMOTION_TYPE),
        )
        return {"label": label, "type": promotion_type}


class PromotionExculdeProductSerializer(DynamicFieldsModelSerializer):
    discount_variant = PromotionDiscountVariantSerializer()

    class Meta:
        model = EcomPromotion
        fields = "__all__"
        # fields = [
        #     "name",
        #     "description",
        #     "link_to",
        #     "thumbnail",
        #     "promotion_type",
        #     "code",
        #     "start_date",
        #     "end_date",
        #     "is_active",
        #     "can_stack",
        #     "discount_variant",
        # ]


# class PromotionThroughSerializer(DynamicFieldsModelSerializer):
#     promotion = PromotionExculdeProductSerializer()

#     class Meta:
#         model = EcomProductPromotionExtra
#         exclude = ["product"]
