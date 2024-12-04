from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from ecommerce.models import EcomCategory
from ecommerce.serializers.dynamic import DynamicFieldsModelSerializer


class BaseCategorySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = EcomCategory
        fields = ["id", "name", "display_name", "name_slug", "parent"]
