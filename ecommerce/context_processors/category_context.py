import logging
import functools

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.urls import reverse

from ecommerce.helpers import find
from ecommerce.models import EcomCategory, EcomStore, EcomStoreGuideline

logger = logging.getLogger(__name__)


def header_footer_context(request):
    try:
        root = EcomCategory.objects.select_related("parent").all()

        def build_tree_recursive(categories, parent_id=None):
            # Find all categories whose parent_id matches the current parent
            sub_category = [
                cat
                for cat in categories
                if cat.parent == parent_id
                or (cat.parent and cat.parent.id == parent_id)
            ]
            tree = []
            for child in sub_category:
                tree.append(
                    {
                        "id": child.id,
                        "name": child.name,
                        "name_slug": child.name_slug,
                        "display_name": child.display_name,
                        "sub_category": build_tree_recursive(
                            categories, child.id
                        ),  # Recursive call
                    }
                )
            return tree

        category_tree = build_tree_recursive(root)

        for_men = find(lambda i: i.get("id") == 12, category_tree)
        sub_category = for_men.get("sub_category") if for_men else list()
        accessories = find(lambda i: i.get("id") == 23, category_tree)
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

        storeSerialized = get_object_or_404(EcomStore, pk=1)

        guidelineSerialized = get_list_or_404(EcomStoreGuideline)

        return {
            "navigations_context": navigations,
            "store_context": storeSerialized,
            "guideline_context": guidelineSerialized,
        }
    except Exception as error:
        logger.error(f"Unhandled error in context processor: {error}")
        return error
