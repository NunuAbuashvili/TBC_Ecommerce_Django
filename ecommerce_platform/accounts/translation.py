from modeltranslation.translator import translator, TranslationOptions

from .models import CustomUser


class CustomUserTranslationOptions(TranslationOptions):
    fields = ('gender', 'account_type', 'country', 'city', 'street_address',)


translator.register(CustomUser, CustomUserTranslationOptions)
