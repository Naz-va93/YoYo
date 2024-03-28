from .models import *
from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

class CoinAdmin(admin.ModelAdmin):
    list_display = ('id', 'coin_name')
    list_display_links = ('id', 'coin_name')
    search_fields = ('id', 'coin_name')
    exclude = ('slug', 'contact_address')

    actions = ['create_multiple_votes_100', 'create_multiple_votes_10', 'create_multiple_votes_1000']

    def create_multiple_votes_100(self, request, queryset):
        for coin in queryset:
            for i in range(100):
                Vote.objects.create(coin=coin)

        self.message_user(request, f"Успешное добавление 1000 голосов {queryset.count()}")

    create_multiple_votes_100.short_description = "Добавления 100 голосов"  # Название действия в админ панели

    def create_multiple_votes_1000(self, request, queryset):
        for coin in queryset:
            for i in range(1000):
                Vote.objects.create(coin=coin)

        self.message_user(request, f"Успешное добавление 1000 голосов {queryset.count()}")

    create_multiple_votes_1000.short_description = "Добавления 1000 голосов"  # Название действия в админ панели

    def create_multiple_votes_10(self, request, queryset):
        for coin in queryset:
            for i in range(10):
                Vote.objects.create(coin=coin)

        self.message_user(request, f"Успешное добавление 10 голосов {queryset.count()}")
    create_multiple_votes_10.short_description = "Добавления 10 голосов"  # Название действия в админ панели


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
    list_display = ('id', 'name', 'email')
    list_display_links = ('id', 'name', 'email')
    search_fields = ('id', 'name', 'email')


class CartColdAdmin(admin.ModelAdmin):
    inlines = [OrderInline]
    list_display = ('id',)
    list_display_links = ('id',)
    search_fields = ('id',)
    exclude = ('live_cart',)


admin.site.register(CartCold, CartColdAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(CreateOrder, CreateOrderAdmin)
admin.site.register(Coin, CoinAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(NetworkChain, NetworkChainAdmin)
admin.site.register(ListingPlatform, ListingPlatformAdmin)
admin.site.register(AdvertisingItem, AdvertisingItemAdmin)
admin.site.register(Social)
admin.site.register(Listing)
admin.site.register(Setting)
