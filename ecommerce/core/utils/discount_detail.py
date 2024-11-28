import functools
from decimal import Decimal

from ecommerce.helpers import find
from ecommerce.models.promotion import EcomPromotion, EcomPromotionDiscountVariant


def discount_detail(product, *, promotion_type=None):
    promotion_detail = find(
        lambda promotion: promotion["promotion_type"]["type"] == promotion_type,
        product["promotions"],
    )

    promotion = dict()
    discounted_price = None
    price = functools.reduce(
        lambda acc, curr: min(acc, Decimal(curr["price"]))
        if acc != 0
        else Decimal(curr["price"]),
        product["variants"],
        0,
    )

    if promotion_detail:
        promotion = promotion_detail
        discount_variant = promotion_detail["discount_variant"]
        promotion_discount_type = discount_variant["discount_type"].get("value")
        promotion_discount_value = discount_variant["discount_value"]

        if (
            promotion_discount_type
            == EcomPromotionDiscountVariant.DISCOUNT_TYPE.percentage
        ):
            discount_rate = Decimal(promotion_discount_value) / 100
            discounted_price = price * (1 - discount_rate)
            return {
                **product,
                "discounted_price": "{:.0f}".format(discounted_price),
                "price": "{:.0f}".format(price),
                "promotions": promotion,
            }
        else:
            return {
                **product,
                "discounted_price": discounted_price,
                "price": "{:.0f}".format(price),
                "promotions": promotion,
            }
    else:
        return {
            **product,
            "discounted_price": discounted_price,
            "price": "{:.0f}".format(price),
            "promotions": product["promotions"][0]
            if product["promotions"]
            else promotion,
        }
