from ecommerce.models import EcomPromotion, EcomProducts, EcomPromotionDiscountVariant
from wrapper import query_debugger
from ecommerce.helpers import find


class PromotionsDiscountHandler:
    def __init__(self, promotions, products):
        self.promotions = promotions
        self.products = products

        self.total_price = 0
        self.total_quantity = 0

    def delivery_promotions(self):
        return [
            item
            for item in self.promotions
            if item["promotion_type"]["type"] == EcomPromotion.PROMOTION_TYPE.freeship
        ]

    def coupon_promotions(self):
        return [
            item
            for item in self.promotions
            if item.get("promotion_type")["type"] == EcomPromotion.PROMOTION_TYPE.coupon
        ]

    def is_numeric(self, value):
        """Check if a value is numeric."""
        try:
            float_value = float(value)
            return float_value != float("inf") and float_value != float("-inf")
        except (ValueError, TypeError):
            return False

    def calculate_discount_value_based_on_discount_type(self, promotion, base_price):
        # Extract discount variant and convert values to float
        discount_variant = promotion.discount_variant

        max_discount = float(discount_variant.max_discount)
        discount_value = float(discount_variant.discount_value)

        # Validate input values
        if not (
            self.is_numeric(base_price)
            and self.is_numeric(max_discount)
            and self.is_numeric(discount_value)
        ):
            raise ValueError("Not a valid number!")

        # Calculate discount based on type
        if (
            discount_variant.discount_type
            == EcomPromotionDiscountVariant.DISCOUNT_TYPE.percentage
        ):  # Adjust key based on actual structure
            result = base_price * discount_value / 100
            result = min(result, max_discount) if max_discount else result
        else:
            result = base_price - discount_value
            result = min(result, max_discount) if max_discount else result

        return result

    def calculate_discount_for_single_product(self, product):
        selected_variant = product.selected_variant
        promotions = product.promotions.all()

        price = {"base_price": 0, "discounted_price": 0}

        basePrice = float(selected_variant.price)
        price["base_price"] = basePrice

        flashsale = find(
            lambda item: item.promotion_type == EcomPromotion.PROMOTION_TYPE.flashsale,
            promotions,
        )
        if flashsale:
            discount = self.calculate_discount_value_based_on_discount_type(
                flashsale, price["base_price"]
            )
            price["discounted_price"] = price["base_price"] - discount
            return price

        product_sale = find(
            lambda item: item.promotion_type == EcomPromotion.PROMOTION_TYPE.product,
            promotions,
        )
        if product_sale:
            discount = self.calculate_discount_value_based_on_discount_type(
                product_sale, price["base_price"]
            )
            price["discounted_price"] = price["base_price"] - discount
            return price
        return price

    def validate_coupon_promotions_based_on_order(self):
        for product in self.products:
            if product.selected_variant:
                price = self.calculate_discount_for_single_product(product)
                self.total_price += (
                    float(price["discounted_price"]) or float(price["base_price"])
                ) * product.selected_variant.quantity
                self.total_quantity += product.selected_variant.quantity

        if not self.total_price or not self.total_quantity:
            raise Exception("total_price & total_quantity cannot be zero!")

        coupon_promotions = self.coupon_promotions()

        for item in coupon_promotions:
            discount_variant = item["discount_variant"]
            # total_quantity = sum(
            #     product["selected_variant"]["quantity"] for product in self.products
            # )

            def is_quantity_satisfied():
                min_item = discount_variant.get("min_item", 0)
                max_item = discount_variant.get("max_item", 0)
                if min_item >= 0 and max_item == 0:
                    return self.total_quantity >= min_item
                elif min_item != 0 and max_item != 0:
                    return min_item <= self.total_quantity <= max_item
                return True

            def is_total_price_satisfied():
                min_purchase = float(discount_variant.get("min_purchase", 0))
                max_purchase = float(discount_variant.get("max_purchase", 0))
                if min_purchase >= 0 and max_purchase == 0:
                    return self.total_price >= min_purchase
                elif min_purchase != 0 and max_purchase != 0:
                    return min_purchase <= self.total_price <= max_purchase
                return True

            item["is_valid"] = is_quantity_satisfied() and is_total_price_satisfied()

        return coupon_promotions
