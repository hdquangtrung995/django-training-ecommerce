from django.db import models
from django.conf import settings

from model_utils.models import TimeStampedModel
from ecommerce.models import EcomCustomerOrder, EcomProducts


class EcomProductReview(TimeStampedModel):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_id = models.ForeignKey(EcomCustomerOrder, on_delete=models.CASCADE)
    product_id = models.ForeignKey(EcomProducts, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    review_text = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "ecom_product_review"
        verbose_name = "product review"
        verbose_name_plural = "product reviews"

    def __str__(self):
        return f"{self.id} {self.user_id} {self.order_id} {self.product_id}"
