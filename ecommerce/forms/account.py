from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AdminPasswordChangeForm
from django.contrib.auth import password_validation

from user.models import EcomUser


class AccountCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    date_of_birth = date_of_birth = forms.DateField(
        label="Birthday", widget=forms.SelectDateWidget(years=range(1980, 2000))
    )
    email_verified = forms.BooleanField(label="Email vefified", required=False)

    class Meta:
        model = EcomUser
        fields = ["email", "phone", "first_name", "last_name", "date_of_birth"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        # try:
        #     password_validation.validate_password(password2, self.instance)
        # except ValidationError as error:
        #     print("error: ", error.messages, type(error.messages))
        #     raise ValidationError(error)
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AccountChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()
    date_of_birth = forms.DateField(
        label="Birthday ",
        widget=forms.SelectDateWidget(years=range(1980, 2000)),
        required=False,
    )
    email_verified = forms.BooleanField(label="Email vefified", required=False)

    class Meta:
        model = EcomUser
        fields = [
            "email",
            "password",
            "date_of_birth",
            "is_active",
            "is_superuser",
            "is_staff",
        ]


class RegisterAccountForm(AccountCreationForm):
    date_of_birth = None
    email_verified = None

    class Meta:
        model = EcomUser
        fields = ["email"]


class LoginAccountForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class AccountChangeWithOutPasswordForm(AccountChangeForm):
    password = None

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "readonly": True,
                "class": "cursor-not-allowed bg-gray-600",
                "style": "background-color: #e0e0e0;",
            }
        )
    )
    first_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "First name"})
    )
    last_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "Last name"})
    )

    email_verified = forms.BooleanField(
        label="Email vefified",
        required=False,
        widget=forms.CheckboxInput(
            attrs={"disabled": True, "class": "cursor-not-allowed"}
        ),
    )
    phone = forms.CharField(
        label="Phone",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Your phone number"}),
    )

    class Meta:
        model = EcomUser
        fields = [
            "email",
            "date_of_birth",
            "first_name",
            "last_name",
            "phone",
            "email_verified",
        ]
