from rest_framework import serializers
from decimal import Decimal
from django.conf import settings

from ecommerce.models import (
    EcomProducts,
    EcomProductPromotionExtra,
    EcomProductVariant,
    EcomPromotion,
    EcomPromotionDiscountVariant,
)
from ecommerce.serializers.dynamic import DynamicFieldsModelSerializer
from ecommerce.serializers import (
    ProductsVariantSerializer,
    PromotionDiscountVariantSerializer,
    # PromotionThroughSerializer,
    # PromotionExculdeProductSerializer,
    # ProductsPriceSerializer,
    BasePromotionSerializer,
)
from ecommerce.helpers import find


class BaseProductsSerializer(DynamicFieldsModelSerializer):
    variants = ProductsVariantSerializer(many=True)
    promotions = BasePromotionSerializer(many=True)
    # promotions = BasePromotionSerializer(
    #     source="ecomproductpromotionextra_set", many=True
    # )

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

    def get_products(self, obj):
        data = obj.products.all()[
            : settings.MY_WEBAPP_SETTING.get("NUMBER_OF_RECORD_FOR_FLASHSALE")
        ]
        # return ProductsPriceSerializer(data, many=True).data
        return []


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
