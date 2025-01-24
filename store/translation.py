from modeltranslation.translator import translator, TranslationOptions

from .models import Tea, Category, Tag


class AbstractStoreTranslationOptions(TranslationOptions):
    fields = ('name',)


class TeaTranslationOptions(AbstractStoreTranslationOptions):
    fields = ('description', 'place_of_origin', 'ingredients',)


class CategoryTranslationOptions(AbstractStoreTranslationOptions):
    fields = ('description',)


translator.register(Tea, TeaTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
translator.register(Tag, AbstractStoreTranslationOptions)
