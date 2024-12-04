from rest_framework import serializers
from ecommerce.models import (
    EcomProductVariant,
)
from ecommerce.helpers import find
from ecommerce.serializers.dynamic import DynamicFieldsModelSerializer


class BaseProductsVariantSerializer(DynamicFieldsModelSerializer):
    size = serializers.SerializerMethodField()

    class Meta:
        model = EcomProductVariant
        fields = "__all__"

    def get_size(self, obj):
        value, label = find(
            lambda item: True if item[0] == obj.size else False,
            list(EcomProductVariant.SIZES),
        )
        return {"value": value, "label": label}
