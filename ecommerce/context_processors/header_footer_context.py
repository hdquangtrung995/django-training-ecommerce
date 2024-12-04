import logging
from ecommerce.helpers import find

logger = logging.getLogger(__name__)


def header_footer_context(request):
    try:

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

        category_tree = build_tree_recursive(request.common_data.get("categories"))

        for_men = find(lambda i: i.get("id") == 12, category_tree)
        sub_category = for_men.get("sub_category") if for_men else list()
        accessories = find(lambda i: i.get("id") == 23, category_tree)
        navigations = [
            {
                "name": "products",
                "display_name": "products",
                "name_slug": "",
                "sub_category": [*sub_category, accessories],
            },
            *sub_category,
            accessories,
        ]
        return {
            "navigations_context": navigations,
            "store_context": request.common_data.get("store_context"),
            "guideline_context": request.common_data.get("guideline_context"),
        }
    except Exception as error:
        logger.error(f"Unhandled error in context processor: {error}")
        return error
