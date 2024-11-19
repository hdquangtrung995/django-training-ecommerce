from rest_framework import serializers
from ecommerce.models import EcomStore, EcomStoreGuideline


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcomStore
        fields = [
            "name",
            "email",
            "description",
            "phone",
            "banners",
            "media_link",
            "logo",
            "open_at",
            "close_at",
        ]


class StoreGuideLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcomStoreGuideline
        fields = ["label", "banner", "content", "slug"]
