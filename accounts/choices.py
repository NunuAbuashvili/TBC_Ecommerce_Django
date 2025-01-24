from django.db import models
from django.utils.translation import gettext_lazy as _

class GenderChoices(models.TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')
    OTHER = 'O', _('Other')
    PREFER_NOT_TO_SAY = 'P', _('Prefer Not To Say')
