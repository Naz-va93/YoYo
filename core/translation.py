from modeltranslation.translator import register, TranslationOptions

from .models import *


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'text_field_1', 'text_field_3', 'text_field_4')


@register(Setting)
class SettingTranslationOptions(TranslationOptions):
    fields = (
    'stat_title', 'stat_text', 'contacts_title', 'copyright', 'footer_text', 'promote_text', 'promote_text_spot',
    'promote_text_banner')


@register(Coin)
class CoinTranslationOptions(TranslationOptions):
    fields = ('coin_description',)


@register(NetworkChain)
class NetworkChainTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Type)
class TypeTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(ListingPlatform)
class ListingPlatformTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Listing)
class ListingTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(ReferenceCurrency)
class ReferenceCurrencyTranslationOptions(TranslationOptions):
    fields = ('name',)
