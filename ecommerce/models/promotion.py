from django.db import models
from model_utils import Choices
from django.utils.translation import gettext_lazy as _


class EcomPromotion(models.Model):
    DISCOUNT_TYPE = Choices(
        (0, "percentage", _("percentage")), (1, "fixed", _("fixed"))
    )
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
    code = models.CharField(max_length=50, blank=False)
    discount_type = models.CharField(choices=DISCOUNT_TYPE, blank=False)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=False)
    can_stack = models.BooleanField(default=False)

    class Meta:
        db_table = "ecom_promotion"
        verbose_name = "promotion"
        verbose_name_plural = "promotions"

    def __str__(self):
        return f"{self.name} {self.code} (id: {self.id})"
