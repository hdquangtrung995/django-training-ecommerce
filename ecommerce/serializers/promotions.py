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

    def get_discount_type(self, obj):
        value, label = find(
            lambda item: True if item[0] == obj.discount_type else False,
            list(EcomPromotionDiscountVariant.DISCOUNT_TYPE),
        )
        return {"value": value, "label": label}


class BasePromotionSerializer(DynamicFieldsModelSerializer):
    discount_variant = PromotionDiscountVariantSerializer()
    promotion_type = serializers.SerializerMethodField()

    class Meta:
        model = EcomPromotion
        fields = "__all__"

    def get_promotion_type(self, obj):
        promotion_type, label = find(
            lambda item: True if item[0] == obj.promotion_type else False,
            list(EcomPromotion.PROMOTION_TYPE),
        )
        return {"label": label, "type": promotion_type}


class PromotionExculdeProductSerializer(DynamicFieldsModelSerializer):
    discount_variant = PromotionDiscountVariantSerializer()

    class Meta:
        model = EcomPromotion
        fields = "__all__"
