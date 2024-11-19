from rest_framework import serializers
from ecommerce.models import EcomProducts, EcomProductVariant
from ecommerce.helpers import find


class ProductsVariantSerializer(serializers.ModelSerializer):
    size = serializers.SerializerMethodField()

    class Meta:
        model = EcomProductVariant
        fields = [
            "size",
            "color",
            "sku",
            "stock",
            "price",
            "gender",
            "product_id",
            "size",
        ]

    def get_size(self, obj):
        _, label = find(
            lambda item: item[1] if item[0] == obj.size else None,
            list(EcomProductVariant.SIZES),
        )
        return label


class ProductsSerializer(serializers.ModelSerializer):
    variants = ProductsVariantSerializer(many=True)

    class Meta:
        model = EcomProducts
        fields = [
            "id",
            "name",
            "description",
            "product_code",
            "slug",
            "thumbnail",
            "is_active",
            "galleries",
            "variants",
            "created",
            "modified",
        ]
