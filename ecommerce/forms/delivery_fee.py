from django import forms

baseClass = "w-full rounded-sm p-2 border-b disabled:cursor-not-allowed"


class DeliveryFeeForm(forms.Form):
    province = forms.MultipleChoiceField(
        label="Province",
        required=True,
        choices=[(0, "N/A")],
        widget=forms.Select(
            attrs={"class": baseClass, "id": "province-option", "disabled": True},
        ),
    )
    district = forms.MultipleChoiceField(
        label="District",
        required=True,
        choices=[(0, "N/A")],
        widget=forms.Select(
            attrs={"class": baseClass, "id": "district-option", "disabled": True},
        ),
    )
    ward = forms.MultipleChoiceField(
        label="Ward",
        required=True,
        choices=[(0, "N/A")],
        widget=forms.Select(
            attrs={"class": baseClass, "id": "ward-option", "disabled": True},
        ),
    )
