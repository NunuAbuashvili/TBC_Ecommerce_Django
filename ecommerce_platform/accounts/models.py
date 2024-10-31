from typing import Any, Dict
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from .choices import GenderChoices


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for handling user creation and superuser creation operations.
    Extends Django's BaseUserManager to support email-based authentication.
    """
    def create_user(self, email: str, password: str, **extra_fields: Dict[str, Any]) -> Any:
        """
        Create and save a regular user with the given email and password.

        Args:
            email: User's email address
            password: User's password
            **extra_fields: Additional fields for the user model

        Returns:
            CustomUser: The created user instance.

        Raises:
            ValueError: If email is empty.
        """
        if not email:
            raise ValueError(_('The Email field should not be empty.'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **extra_fields: Dict[str, Any]) -> Any:
        """
        Create and save a superuser with the given email and password.

        Args:
            email: Superuser's email address
            password: Superuser's password
            **extra_fields: Additional fields for the user model

        Returns:
            CustomUser: The created superuser instance.

        Raises:
            ValueError: If is_staff or is_superuser is not True.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser with additional fields.

    Attributes:
        user_id (AutoField): Primary key for the user
        email (EmailField): Unique email address
        phone_number (str): Optional phone number
        date_of_birth (Date): Optional date of birth
        gender (str): Optional gender identity
        is_verified (bool): Email verification status
        account_type (str): Type of account (individual/company)
        country (str): Optional country of residence
        city (str): Optional city of residence
        street_address (str): Optional street address
        postal_code (str): Optional postal code
        newsletter_subscription (bool): Newsletter subscription status
    """
    # User ID
    user_id = models.AutoField(primary_key=True)

    # Contact information
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(_('phone number'), max_length=13, blank=True)

    # Account details
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    gender = models.CharField(
        max_length=2,
        choices=GenderChoices,
        default=GenderChoices.PREFER_NOT_TO_SAY,
    )
    is_verified = models.BooleanField(_('email verified'), default=False)
    account_type = models.CharField(
        _('account type'),
        max_length=20,
        choices=[
            ('individual', 'Individual'),
            ('company', 'Company'),
        ],
        default='individual',
    )

    # Address information
    country = CountryField(blank_label="Select country")
    city = models.CharField(_('city'), max_length=100, blank=True)
    street_address = models.CharField(_('street address'), max_length=255, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=10, blank=True)

    # Marketing Preferences
    newsletter_subscription = models.BooleanField(_('newsletter subscription'), default=False)

    # Additional information for database
    last_active_datetime = models.DateTimeField(_('last active'), auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
