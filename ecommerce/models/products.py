import datetime

from django.db import models
from ecommerce.models.abstracts import UUIDBaseModel
from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify
from model_utils.models import TimeStampedModel
from django.utils import timezone

from ecommerce.models import EcomCategory, EcomPromotion


# Create your models here.
class EcomProducts(UUIDBaseModel, TimeStampedModel):
    MAXIMUM_GALLERY_ITEMS = 6

    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True, null=True)
    product_code = models.CharField(max_length=50, null=True, blank=False)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    thumbnail = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, default=False)
    galleries = ArrayField(models.URLField(max_length=255), size=MAXIMUM_GALLERY_ITEMS)
    category = models.ForeignKey(EcomCategory, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "ecom_products"
        verbose_name = "product"
        verbose_name_plural = "products"

    def __str__(self):
        return f"{self.name} (id: {self.id})"

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def was_added_recently(self):
        """New products added recently

        Returns:
            boolean: New Product
        """
        return self.is_active and self.created >= timezone.now() - datetime.timedelta(
            days=1
        )


class EcomProductPromotionJoinTable(models.Model):
    product = models.ForeignKey(EcomProducts, on_delete=models.CASCADE)
    promotion = models.ForeignKey(EcomPromotion, on_delete=models.CASCADE)

    class Meta:
        db_table = "ecom_product_promotion_join_table"
        verbose_name = "Product Promotion Join Table"
        verbose_name_plural = "Product Promotion Join Table"

    def __str__(self):
        return f"{self.product} (id: {self.promotion})"
