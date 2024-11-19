from django.db import models
from model_utils import Choices
from django.utils.translation import gettext_lazy as _
from ecommerce.models import EcomCustomerOrder


class EcomPayment(models.Model):
    PAYMENT_METHOD = Choices(
        (0, "cod", _("cod")),
        (1, "credit_card", _("credit card")),
        (2, "qr_code", _("qr code")),
        (3, "momo", _("momo")),
    )
    PAYMENT_STATUS = Choices(
        (0, "pending", _("pending")),
        (1, "complete", _("complete")),
        (2, "failed", _("failed")),
    )

    order_id = models.OneToOneField(
        EcomCustomerOrder, on_delete=models.CASCADE, primary_key=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(choices=PAYMENT_METHOD, blank=False)
    payment_status = models.CharField(
        choices=PAYMENT_STATUS, default=PAYMENT_STATUS.pending
    )
    transaction_id = models.CharField(max_length=100)
    payment_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "ecom_customer_payment"
        verbose_name = "payment"
        verbose_name_plural = "payments"

    def __str__(self):
        return f"{self.order_id} (id: {self.amount})"
