from django.db import models
from model_utils import Choices
from django.utils.translation import gettext_lazy as _
from datetime import datetime


class PromotionActiveAndNotExpire(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                is_active=True,
                start_date__lte=datetime.now().date(),
                end_date__gte=datetime.now().date(),
            )
        )


# Mimic shopee behavior
# PROMOTION_TYPE.product and PROMOTION_TYPE.flashsale will apply discount on product instance
# PROMOTION_TYPE.coupon and PROMOTION_TYPE.freeship will display as coupon for user to choose at checkout step


class EcomPromotion(models.Model):
    PROMOTION_TYPE = Choices(
        (0, "product", _("product")),
        (1, "coupon", _("coupon")),
        (2, "flashsale", _("flash sale")),
        (3, "freeship", _("free ship")),
    )

    name = models.CharField(max_length=50, null=True)
    description = models.TextField(blank=True, null=True)
    link_to = models.CharField(max_length=250, blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)

    promotion_type = models.IntegerField(choices=PROMOTION_TYPE, null=True, blank=True)
    code = models.CharField(max_length=50, unique=True, blank=False)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    is_active = models.BooleanField(default=False)
    can_stack = models.BooleanField(default=False)

    objects = models.Manager()
    active = PromotionActiveAndNotExpire()

    class Meta:
        db_table = "ecom_promotion"
        verbose_name = "promotion"
        verbose_name_plural = "promotions"

    def __str__(self):
        return f"{self.name} {self.code} (id: {self.id})"


class EcomPromotionDiscountVariant(models.Model):
    DISCOUNT_TYPE = Choices((0, "percentage", _("%")), (1, "fixed", _("k")))

    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    min_item = models.PositiveSmallIntegerField(default=0)
    max_item = models.PositiveSmallIntegerField(default=0)

    min_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    discount_type = models.IntegerField(choices=DISCOUNT_TYPE, blank=False)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)

    promotion = models.OneToOneField(
        EcomPromotion,
        on_delete=models.CASCADE,
        related_name="discount_variant",
        null=True,
    )

    class Meta:
        db_table = "ecom_promotion_discount_variant"
        verbose_name = "promotion discount variant"
        verbose_name_plural = "promotion discount variants"

    def __str__(self):
        return f"id: {self.id}"


# discount_variant
