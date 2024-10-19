from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import *
from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin


class CoinAdmin(admin.ModelAdmin):
    list_display = ('id', 'coin_name', 'is_read_by_admin')
    list_display_links = ('id', 'coin_name')
    search_fields = ('id', 'coin_name')
    exclude = ('slug', 'contact_address', 'is_read_by_admin')
    list_filter = ('is_read_by_admin',)

    actions = ['create_multiple_votes_100', 'create_multiple_votes_10', 'create_multiple_votes_1000']

    def create_multiple_votes_100(self, request, queryset):
        for coin in queryset:
            for i in range(100):
                Vote.objects.create(coin=coin)

        self.message_user(request, f"Успешное добавление 100 голосов {queryset.count()}")

    create_multiple_votes_100.short_description = "Добавления 100 голосов"

    def create_multiple_votes_1000(self, request, queryset):
        for coin in queryset:
            for i in range(1000):
                Vote.objects.create(coin=coin)

        self.message_user(request, f"Успешное добавление 1000 голосов {queryset.count()}")

    create_multiple_votes_1000.short_description = "Добавления 1000 голосов"

    def create_multiple_votes_10(self, request, queryset):
        for coin in queryset:
            for i in range(10):
                Vote.objects.create(coin=coin)

        self.message_user(request, f"Успешное добавление 10 голосов {queryset.count()}")

    create_multiple_votes_10.short_description = "Добавления 10 голосов"

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj and not obj.is_read_by_admin:
            obj.mark_as_read_by_admin()

        return super().change_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.is_read_by_admin = True
        super().save_model(request, obj, form, change)


class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'order')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


class NetworkChainAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'order')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


class ListingPlatformAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


class PageAdmin(admin.ModelAdmin):
    list_display = ('title_seo', 'slug')
    list_display_links = ('title_seo', 'slug')
    search_fields = ('title_seo', 'slug')


class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


class OrderInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class CreateOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'received', 'remaining')
    list_display_links = ('id',)
    search_fields = ('id',)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_display_links = ('id',)
    search_fields = ('id',)
    exclude = ('cart',)


class AdvertisingItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'is_read_by_admin')
    list_display_links = ('id', 'name', 'email')
    search_fields = ('id', 'name', 'email')
    exclude = ('is_read_by_admin',)
    list_filter = ('is_read_by_admin',)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj and not obj.is_read_by_admin:
            obj.mark_as_read_by_admin()

        return super().change_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.is_read_by_admin = True
        super().save_model(request, obj, form, change)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'coin', 'type')
    list_display_links = ('id', 'user', 'coin', 'type')
    search_fields = ('id', 'user', 'coin', 'type')


class CartColdAdmin(admin.ModelAdmin):
    inlines = [OrderInline]
    list_display = ('id',)
    list_display_links = ('id',)
    search_fields = ('id',)
    exclude = ('live_cart',)


class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'show')
    list_display_links = ('id', 'location')
    list_editable = ('show',)


class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class CoinExchangeAdmin(admin.ModelAdmin):
    list_display = ('coin', 'exchange', 'url')
    list_filter = ('coin', 'exchange')
    search_fields = ('coin__name', 'exchange__name')


class ReferenceCurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'symbol')
    list_display_links = ('id', 'name', 'symbol')
    search_fields = ('id', 'name', 'symbol', 'uuid')
    exclude = ('price_to_usd',)


admin.site.register(Coin, CoinAdmin)
admin.site.register(CoinExchange, CoinExchangeAdmin)
admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(NetworkChain, NetworkChainAdmin)
admin.site.register(ListingPlatform, ListingPlatformAdmin)
admin.site.register(AdvertisingItem, AdvertisingItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(ReferenceCurrency, ReferenceCurrencyAdmin)
admin.site.register(Social)
admin.site.register(Listing)
admin.site.register(Setting)
