from django import forms
from django.core.exceptions import ValidationError

from ecommerce.models import EcomPromotion


class PromotionChangeForm(forms.ModelForm):
    class Meta:
        model = EcomPromotion
        fields = "__all__"


class PromotionAddForm(forms.ModelForm):
    class Meta:
        model = EcomPromotion
        fields = "__all__"
