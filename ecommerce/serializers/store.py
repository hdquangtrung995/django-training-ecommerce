from rest_framework import serializers
from ecommerce.models import EcomStore, EcomStoreGuideline
from ecommerce.serializers.dynamic import DynamicFieldsModelSerializer


class BaseStoreSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = EcomStore
        fields = "__all__"


class StoreGuideLineSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = EcomStoreGuideline
        fields = "__all__"
