import random
import functools
from datetime import datetime, timedelta

from django.views.generic import TemplateView
from django.conf import settings
from django.db.models import Prefetch, Q, F, Window
from django.db.models.functions import RowNumber

from ecommerce.core.utils.discount_detail import discount_detail
from ecommerce.serializers import (
    BaseProductsSerializer,
    BasePromotionSerializer,
    ProductPromotionExtraExcludeGalleriesSerializer,
)
from ecommerce.models import (
    EcomProducts,
    EcomPromotion,
    EcomProductPromotionExtra,
)
from ecommerce.helpers import find
from wrapper import query_debugger


# Create your views here.
class HomeView(TemplateView):
    template_name = "ecommerce/page/home/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            current_datetime = datetime.now()
            one_month = current_datetime - timedelta(days=60)
            start_of_month = datetime.now().replace(day=1)
            end_of_month = start_of_month.replace(
                month=start_of_month.month % 12 + 1, day=1
            ) - timedelta(days=1)

            context["list_banners"] = self.get_home_page_banners()
            context["list_of_promotions"] = self.get_home_page_promotions()
            context["flashsale_products"] = self.get_flash_sale_products()
            context["new_products"] = self.recently_added_products(
                created__gt=one_month
            )
            context["recently_added_this_month"] = self.recently_added_products(
                created__range=(start_of_month, end_of_month)
            )
            context["products_by_category"] = self.group_product_by_categories()

        except Exception as error:
            print("__name__: ", __name__, error)
            context["error"] = f"An unexpected error occurred: {str(error)}"
        return context

    def get_home_page_banners(self):
        store = self.request.common_data.get("store_context")
        return store.banners

    def get_home_page_promotions(self):
        current_day = datetime.now().date()
        promotions = EcomPromotion.objects.select_related("discount_variant").filter(
            is_active=True, start_date__lte=current_day, end_date__gte=current_day
        )[: settings.MY_WEBAPP_SETTING.get("NUMBER_OF_RECORD_FOR_HOME_PAGE_PROMOTION")]
        serialized = BasePromotionSerializer(promotions, many=True)

        return serialized.data

    def get_flash_sale_products(self):
        current_datetime = datetime.now()
        current_date = current_datetime.date()

        flashsale_products_prefetch = Prefetch(
            "product",
            queryset=EcomProducts.objects.prefetch_related(
                "variants", "promotions", "promotions__discount_variant"
            ).filter(
                promotions__promotion_type=EcomPromotion.PROMOTION_TYPE.flashsale,
                promotions__start_date__lte=current_date,
                promotions__end_date__gte=current_date,
            ),
        )

        flashsale_products_lookup = EcomProductPromotionExtra.objects.filter(
            promotion__promotion_type=EcomPromotion.PROMOTION_TYPE.flashsale,
            promotion__start_date__lte=current_date,
            promotion__end_date__gte=current_date,
            product__is_active=True,
        ).prefetch_related(flashsale_products_prefetch)[
            : settings.MY_WEBAPP_SETTING.get("NUMBER_OF_RECORD_FOR_FLASHSALE")
        ]
        flashsale_products_serializer = ProductPromotionExtraExcludeGalleriesSerializer(
            flashsale_products_lookup, many=True, exclude=["promotion", "id"]
        )

        def callback(item):
            return discount_detail(
                item, promotion_type=EcomPromotion.PROMOTION_TYPE.flashsale
            )

        flashsale_products = list(
            map(
                callback,
                map(lambda item: item["product"], flashsale_products_serializer.data),
            )
        )
        return flashsale_products

    def recently_added_products(self, q_object=Q(), **fields_lookup):
        """
        Get n new products in each category
        """

        new_products_lookup = (
            EcomProducts.objects.filter(q_object, is_active=True, **fields_lookup)
            .prefetch_related("variants", "promotions", "promotions__discount_variant")
            .annotate(
                rank=Window(
                    expression=RowNumber(),
                    partition_by=[F("category_id")],
                    order_by=F("created").desc(),
                )
            )
            .filter(
                rank__lte=settings.MY_WEBAPP_SETTING.get(
                    "NUMBER_OF_NEW_PRODUCTS_EVERYDAY_IN_EACH_CATEGORY"
                ),
            )
            .order_by("category_id", "rank")[
                : settings.MY_WEBAPP_SETTING.get(
                    "NUMBER_OF_NEW_PRODUCTS_EVERYDAY_FOR_HOMEPAGE"
                )
            ]
        )

        new_products_serializer = BaseProductsSerializer(
            new_products_lookup, many=True, exclude=["galleries"]
        )

        new_products = list(map(discount_detail, new_products_serializer.data))
        random.shuffle(new_products)
        return new_products

    def group_product_by_categories(self):
        product_by_category_lookup = (
            EcomProducts.objects.filter(is_active=True)
            .prefetch_related("variants", "promotions", "promotions__discount_variant")
            .annotate(
                rank=Window(
                    expression=RowNumber(),
                    partition_by=[F("category_id")],
                )
            )
            .filter(rank__lte=6)
            .exclude(category_id__in=[24, 25, 26, 27])
        )
        product_by_category_serializer = BaseProductsSerializer(
            product_by_category_lookup, many=True, exclude=["galleries"]
        )

        def grouping(acc, curr):
            category_id = curr.get("category")

            if category_at_acc := acc.get(category_id):
                if category_at_acc.get("label"):
                    return {
                        **acc,
                        curr.get("category"): {
                            **acc[category_id],
                            "data": [*acc[category_id].get("data"), curr],
                        },
                    }
                else:
                    existing_category = find(
                        lambda category: category.id == category_id,
                        self.request.common_data.get("categories"),
                    )

                    return {
                        **acc,
                        curr.get("category"): {
                            **acc[category_id],
                            "label": existing_category.display_name or "",
                            "slug": f"/{existing_category.name_slug}"
                            if existing_category.name_slug
                            else "#",
                            "data": [*acc[category_id].get("data"), curr],
                        },
                    }
            else:
                return {**acc, category_id: {"label": "", "slug": "#", "data": [curr]}}

        products_by_category = functools.reduce(
            grouping, map(discount_detail, product_by_category_serializer.data), {}
        )
        return products_by_category.values()
