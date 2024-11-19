import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Defines how the User(or the model to which attached)
    will create users and superusers.
    """

    def create_user(self, email, password, date_of_birth, **extra_fields):
        """
        Create and save a user with the given email, password,
        and date_of_birth.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)  # lowercase the domain
        user = self.model(date_of_birth=date_of_birth, email=email, **extra_fields)
        user.set_password(password)  # hash raw password and set
        user.save()
        return user

    def create_superuser(self, email, password, date_of_birth, **extra_fields):
        """
        Create and save a superuser with the given email,
        password, and date_of_birth. Extra fields are added
        to indicate that the user is staff, active, and indeed
        a superuser.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, date_of_birth, **extra_fields)


# Create your models here.
class EcomUser(AbstractUser):
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "date_of_birth"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(_("phone number"), max_length=25, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.URLField(max_length=255, blank=True)
    date_of_birth = models.DateField(verbose_name="Birthday", null=True)

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}, {self.first_name}"
