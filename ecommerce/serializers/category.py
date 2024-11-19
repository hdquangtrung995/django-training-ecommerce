from rest_framework import serializers
from ecommerce.models import EcomCategory
from rest_framework_recursive.fields import RecursiveField


class CategorySerializer(serializers.ModelSerializer):
    sub_category = RecursiveField(allow_null=True, many=True)

    class Meta:
        model = EcomCategory
        fields = ["id", "name", "display_name", "name_slug", "sub_category"]
