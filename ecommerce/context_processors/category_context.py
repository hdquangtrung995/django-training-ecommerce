import logging
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.urls import reverse

from ecommerce.helpers import find
from ecommerce.models import EcomCategory, EcomStore, EcomStoreGuideline
from ecommerce.serializers import (
    CategorySerializer,
    StoreSerializer,
    StoreGuideLineSerializer,
)

logger = logging.getLogger(__name__)


def header_footer_context(request):
    try:
        root = get_list_or_404(EcomCategory, parent=None)
        categories = CategorySerializer(root, many=True).data
        for_men = find(lambda i: i.get("id") == 12, categories)
        sub_category = for_men.get("sub_category") if for_men else list()
        accessories = find(lambda i: i.get("id") == 23, categories)

        navigations = [
            {
                "name": "products",
                "display_name": "products",
                "name_slug": "products",
                "sub_category": [*sub_category, accessories],
            },
            *sub_category,
            accessories,
        ]
        store = get_object_or_404(EcomStore, pk=1)
        storeSerialized = StoreSerializer(store)

        guideline = get_list_or_404(EcomStoreGuideline)
        guidelineSerialized = StoreGuideLineSerializer(guideline, many=True)

        return {
            "navigations_context": navigations,
            "store_context": storeSerialized.data,
            "guideline_context": guidelineSerialized.data,
        }
    except Exception as error:
        logger.error(f"Unhandled error in context processor: {error}")
        return error
