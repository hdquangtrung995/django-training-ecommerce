from rest_framework import serializers
from decimal import Decimal
from django.conf import settings

from ecommerce.models import (
    EcomProducts,
    EcomProductPromotionExtra,
    EcomPromotion,
    EcomPromotionDiscountVariant,
)
from ecommerce.serializers.dynamic import DynamicFieldsModelSerializer
from ecommerce.serializers import (
    BaseProductsVariantSerializer,
    PromotionDiscountVariantSerializer,
    BasePromotionSerializer,
    BaseCategorySerializer,
)
from ecommerce.helpers import find


class BaseProductsSerializer(DynamicFieldsModelSerializer):
    variants = BaseProductsVariantSerializer(many=True)
    promotions = BasePromotionSerializer(many=True)

    class Meta:
        model = EcomProducts
        fields = "__all__"


class PromotionFlashsaleSerializer(DynamicFieldsModelSerializer):
    discount_variant = PromotionDiscountVariantSerializer()
    promotion_type = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = EcomPromotion
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        discount_variant = representation["discount_variant"]
        discount_type = discount_variant["discount_type"].get("value")
        discount_value = discount_variant["discount_value"]

        if discount_type != EcomPromotionDiscountVariant.DISCOUNT_TYPE.percentage:
            raise Exception("Wrong discount type!")

        discount_rate = Decimal(discount_value) / 100
        data = representation["products"]

        def callback(item):
            discounted_price = Decimal(item["price"]) * (1 - discount_rate)
            return {
                **item,
                "discounted_price": "{:.0f}".format(discounted_price),
                "price": "{:.0f}".format(Decimal(item["price"])),
            }

        return {**representation, "products": list(map(callback, data))}

    def get_promotion_type(self, obj):
        _, label = find(
            lambda item: item[1] if item[0] == obj.promotion_type else None,
            list(EcomPromotion.PROMOTION_TYPE),
        )
        return label


class ProductPromotionExtraSerializer(DynamicFieldsModelSerializer):
    product = BaseProductsSerializer()
    promotion = BasePromotionSerializer()

    class Meta:
        model = EcomProductPromotionExtra
        fields = "__all__"


class ProductPromotionExtraExcludeGalleriesSerializer(ProductPromotionExtraSerializer):
    product = BaseProductsSerializer(exclude=["galleries"])

    class Meta:
        model = EcomProductPromotionExtra
        fields = "__all__"


class ProductWithCategorySerializer(BaseProductsSerializer):
    category = BaseCategorySerializer(exclude=["parent"])

    class Meta:
        model = EcomProducts
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            **representation,
            "variants": [
                {**i, "product": str(i.get("product"))}
                for i in representation.get("variants")
            ],
        }
