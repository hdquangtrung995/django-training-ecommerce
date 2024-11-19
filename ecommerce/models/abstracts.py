import uuid

from django.db import models
from model_utils.fields import UUIDField


class UUIDBaseModel(models.Model):
    id = UUIDField(primary_key=True, version=4, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True
