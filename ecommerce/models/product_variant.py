from django.db import models
from model_utils import Choices
from django.utils.translation import gettext_lazy as _

from ecommerce.models import EcomProducts


class EcomProductVariant(models.Model):
    SIZES = Choices(
        (0, "xs", _("XS")),
        (1, "s", _("S")),
        (2, "m", _("M")),
        (3, "l", _("L")),
        (4, "xl", _("XL")),
        (5, "xxl", _("XXl")),
    )
    GENDER = Choices(
        (0, "male", _("male")),
        (1, "female", _("female")),
        (2, "unisex", _("unisex")),
    )

    size = models.IntegerField(choices=SIZES, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    sku = models.CharField(max_length=100, null=True, blank=True)
    stock = models.PositiveSmallIntegerField(default=0, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(choices=GENDER, blank=False)
    product = models.ForeignKey(
        EcomProducts, on_delete=models.CASCADE, related_name="variants"
    )

    class Meta:
        db_table = "ecom_product_variant"
        verbose_name = "product variant"
        verbose_name_plural = "product variants"

    def __str__(self):
        return f"Product ID: {self.product} (id: {self.id})"
