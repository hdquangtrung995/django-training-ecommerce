from django.db import models
from model_utils import Choices
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from ecommerce.models.abstracts import UUIDBaseModel
from ecommerce.models import EcomProductVariant


class EcomCustomerOrder(UUIDBaseModel):
    ORDER_STATUS = Choices(
        (0, "inprogress", _("in progress")),
        (1, "checkout", _("check out")),
        (2, "placed", _("placed")),
        (3, "complete", _("complete")),
        (4, "canceled", _("canceled")),
    )

    order_status = models.CharField(
        choices=ORDER_STATUS, default=ORDER_STATUS.inprogress
    )
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.CharField(max_length=300, blank=False)
    shipping_city = models.CharField(max_length=100, blank=False)
    placed_at = models.DateField(blank=True, null=True)
    customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = "ecom_customer_order"
        verbose_name = "order"
        verbose_name_plural = "orders"

    def __str__(self):
        return f"{self.code} (id: {self.id})"


class EcomOrderItem(models.Model):
    order_id = models.ForeignKey(EcomCustomerOrder, on_delete=models.CASCADE)
    variant_id = models.ForeignKey(EcomProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "ecom_order_item"
        verbose_name = "order item"
        verbose_name_plural = "order items"

    def __str__(self):
        return f"{self.order_id} (id: {self.variant_id})"
