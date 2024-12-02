import random
import functools
from datetime import datetime, timedelta

from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, get_list_or_404
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
    EcomStore,
    EcomCategory,
    EcomPromotion,
    EcomProductPromotionExtra,
)
from ecommerce.helpers import find
from wrapper import query_debugger


# Create your views here.
class HomeView(TemplateView):
    template_name = "ecommerce/page/home/index.html"

    def get_context_data(self, *args, **kwargs):
        # return HttpResponse(reverse("ecommerce:home_page"))
        try:
            context = super().get_context_data(*args, **kwargs)

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

            return context

            # abc = [
            #     "41ec64d1-27fc-4d88-b874-c6b6743d9fd3",
            #     "b82106f5-25ea-4b5f-a036-68698762b79e",
            #     "3a722724-3967-4cdd-8ee7-abfd1f372aba",
            #     "2e8ca773-2979-4d0d-a4f3-65d75deeb905",
            #     "1df89b00-f51d-417d-bc67-e4e4ed41b711",
            #     "cf50c69d-cc73-4edd-82e7-1ece1f310f25",
            #     "0ef46993-bb05-41a7-b953-46aeaa42ae86",
            #     "558e134b-4975-44dd-baa6-044ed6f997fd",
            #     "17d6fd36-7dd0-47e9-a7b7-aecfbec5d8f2",
            #     "64f217cf-cdd2-4f39-9ee9-257c5d31d2ee",
            #     "306a4543-cf13-4dca-9843-03026af5781d",
            # ]
            # products = EcomProducts.objects.filter(id__in=abc)
            # promo = EcomPromotion.objects.get(pk=6)

            # product = EcomProducts.objects.get(
            #     pk="8ac9bf99-29f4-45d6-abf4-b590335e944d"
            # )
            # seri = PromotionSerializer(promo)
            # product.promotions.add(promo)
            # print("product: ", seri.data)

            # promo = EcomPromotion.objects.get(pk=9)
            # vari = EcomPromotionDiscountVariant.objects.get(pk=4)
            # vari.promotion = promo
            # vari.save()

            # for shirt in shirts:
            #     # print("shirt: ", shirt)
            #     vari = EcomProductVariant(
            #         size=EcomProductVariant.SIZES.s,
            #         color="black",
            #         sku=generate_sku(prefix="SKU"),
            #         stock=3,
            #         price=300000.00,
            #         gender=EcomProductVariant.GENDER.male,
            #         product_id=shirt,
            #     )
            #     empty.append(vari)

            # product = EcomProducts.objects.prefetch_related("variants").get(
            #     pk="0aef564b-6132-41c6-81c5-ef1f0d27dc45"
            # )
            # print("product: ", ProductsSerializer(product).data)

            # current = datetime.now()
            # delta = timedelta(days=14)
            # promo = EcomPromotion(
            #     name="giảm 80k",
            #     description="đơn từ 999k (số lượng có hạn)",
            #     # link_to="/",
            #     # thumbnail="https://file.hstatic.net/1000253775/file/voucher_ao_thun.png",
            #     promotion_type=EcomPromotion.PROMOTION_TYPE.product,
            #     # code=generate_sku(prefix="FLASH"),
            #     code="WIN80",
            #     start_date=current.date(),
            #     end_date=current + delta,
            #     is_active=True,
            #     can_stack=False,
            # )
            # promo.save()

            # return HttpResponse(
            #     render(
            #         request,
            #         self.template_name,
            #         {
            #             "list_banners": banners,
            #             "list_of_promotions": list_of_promotions,
            #             "flashsale_products": homepage["flashsale_products"],
            #             "new_products": homepage["new_products"],
            #             "recently_added_this_month": homepage[
            #                 "recently_added_this_month"
            #             ],
            #             "products_by_category": homepage["products_by_category"],
            #             "list_banners": [],
            #             "list_of_promotions": [],
            #             "flashsale_products": [],
            #             "new_products": [],
            #         },
            #     )
            # )
        except Exception as e:
            print("error: ", e)
            return 404

    def get_home_page_banners(self):
        store = self.request.common_data.get("store_context")
        return store.banners

    def get_home_page_promotions(self):
        current_day = datetime.now().date()
        promotions = get_list_or_404(
            EcomPromotion.objects.select_related("discount_variant").filter(
                is_active=True, start_date__lte=current_day, end_date__gte=current_day
            )[
                : settings.MY_WEBAPP_SETTING.get(
                    "NUMBER_OF_RECORD_FOR_HOME_PAGE_PROMOTION"
                )
            ]
        )
        serialized = BasePromotionSerializer(promotions, many=True)

        return serialized.data

    def get_flash_sale_products(self):
        current_datetime = datetime.now()
        current_date = current_datetime.date()

        active_products = EcomProductPromotionExtra.objects.filter(
            product__is_active=True
        )
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
        flashsale_products_lookup = active_products.prefetch_related(
            flashsale_products_prefetch
        )[: settings.MY_WEBAPP_SETTING.get("NUMBER_OF_RECORD_FOR_FLASHSALE")]
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
        # category_lookup = EcomCategory.objects.all()

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
