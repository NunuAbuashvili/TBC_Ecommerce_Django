from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


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
        _('gender'),
        max_length=2,
        blank=True,
        null=True,
        choices=[
            ('M', 'Male'),
            ('F', 'Female'),
            ('O', 'Other'),
            ('P', 'Prefer not to say')
        ],
        help_text=_('Optional field for gender identity')
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
    country = models.CharField(_('country'), max_length=100, blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    street_address = models.CharField(_('street address'), max_length=255, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=10, blank=True)

    # Marketing Preferences
    newsletter_subscription = models.BooleanField(_('newsletter subscription'), default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
