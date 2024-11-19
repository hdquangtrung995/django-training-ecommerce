from django.db import models
from django.contrib.postgres.fields import ArrayField


class EcomStore(models.Model):
    name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(blank=False)
    description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True)
    banners = ArrayField(models.JSONField(), default=list)
    media_link = ArrayField(models.JSONField(), default=list)
    logo = models.CharField(blank=True, null=True)
    open_at = models.CharField(blank=False, null=True)
    close_at = models.CharField(blank=False, null=True)

    class Meta:
        db_table = "ecom_store"
        verbose_name = "store"
        verbose_name_plural = "stores"

    def __str__(self):
        return f"{self.id} {self.name} {self.email}"


class EcomStoreBranch(models.Model):
    branch_name = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=255, blank=False)
    phone = models.CharField(max_length=50, blank=False)
    email = models.EmailField(blank=True)
    store = models.ForeignKey(EcomStore, on_delete=models.CASCADE)

    class Meta:
        db_table = "ecom_store_branch"
        verbose_name = "store branch"
        verbose_name_plural = "store branches"

    def __str__(self):
        return f"{self.id} {self.name} {self.email}"


class EcomStoreGuideline(models.Model):
    label = models.CharField(blank=False)
    banner = models.CharField(blank=False)
    content = models.CharField(blank=False)
    slug = models.SlugField(default="")

    class Meta:
        db_table = "ecom_store_guideline"
        verbose_name = "store guideline"
        verbose_name_plural = "store guideline"

    def __str__(self):
        return f"{self.id} {self.label}"
