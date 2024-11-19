from django.db import models
from django.utils.text import slugify


class EcomCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    display_name = models.CharField(max_length=100, blank=False, null=False, default="")
    name_slug = models.SlugField(
        max_length=200, blank=True, unique=True, editable=False, null=True
    )
    parent = models.ForeignKey(
        "self", null=True, on_delete=models.SET_NULL, related_name="sub_category"
    )

    class Meta:
        db_table = "ecom_category"
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.name} (id: {self.id})"

    def save(self, *args, **kwargs):
        if not self.id:
            self.name_slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)
