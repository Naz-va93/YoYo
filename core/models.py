from datetime import datetime, timedelta, date
from decimal import Decimal

from ckeditor.fields import RichTextField
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import pre_save, post_migrate
from django.dispatch import receiver
from django.urls import reverse
from slugify import slugify
from django.utils import timezone
from django.db.models import Count, Q, When, Case, BooleanField


class NetworkChain(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name='Название')
    slug = models.SlugField(max_length=100, blank=True, null=True)
    photo = models.FileField(blank=False, null=True, verbose_name='Фото')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(NetworkChain, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:coin-list-chain', kwargs={'slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name='Название')
    slug = models.SlugField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:coin-list-category', kwargs={'slug': self.slug})


class Type(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name='Название')
    slug = models.SlugField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Type, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:coin-list-type', kwargs={'slug': self.slug})


class ListingPlatform(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name='Название')

    def __str__(self):
        return self.name


class Coin(models.Model):
    # seo
    title_seo = models.CharField(max_length=150, blank=True, null=True, verbose_name='Название для seo')
    description_seo = models.CharField(max_length=250, blank=True, null=True, verbose_name='Описание для seo')

    # for form only
    coin_name = models.CharField(max_length=50, blank=False, verbose_name='Название')
    coin_symbol = models.CharField(max_length=10, blank=False, verbose_name='Абревиатура коина')
    listing_link = models.URLField(blank=True, verbose_name='Ссылка на листинг')
    contact_address = models.CharField(max_length=100, verbose_name='Контактный адрес')
    coin_description = models.TextField(max_length=1000, blank=False, verbose_name='Описание коина')
    website_link = models.URLField(blank=False)
    twitter_link = models.URLField(blank=True)
    telegram_link = models.URLField(blank=True)
    discord_link = models.URLField(blank=True)
    telegram_contact = models.CharField(max_length=250, blank=True)
    reddit_link = models.URLField(blank=True)
    photo_coin = models.FileField(blank=False, verbose_name='Фото')

    # ForeignKey
    category = models.ForeignKey('Category', on_delete=models.PROTECT, blank=True, null=True, verbose_name='Категория')
    listing_platform = models.ForeignKey('ListingPlatform', on_delete=models.PROTECT, blank=True, null=True,
                                         verbose_name='Платформа листинга')
    network_chain = models.ForeignKey('NetworkChain', on_delete=models.PROTECT, blank=True, null=True,
                                      verbose_name='Сеть')
    type_project = models.ForeignKey('Type', on_delete=models.PROTECT, blank=True, null=True,
                                     verbose_name='Cетевая цепочка')
    favorite = models.ManyToManyField('user.User', blank=True)

    # coin detail
    binance_smart_chain = models.CharField(null=True, blank=True, verbose_name='Контрактный адрес')
    market_cap = models.FloatField(null=True, blank=True, default=0.00, verbose_name='Капитализация')
    price = models.FloatField(null=True, blank=True, default=0.00, verbose_name='Цена')
    price_24h = models.FloatField(null=True, blank=True, default=0.00, verbose_name='Цена за 24 часа')
    is_api = models.BooleanField(blank=False, null=True, verbose_name='Статус api')
    promoted_status = models.BooleanField(blank=False, null=True, default=False, verbose_name='Статус продвижения')
    is_moderate = models.BooleanField(blank=False, null=True, default=False, verbose_name='Статус модерации')
    uuid = models.CharField(blank=True, null=True)
    counter_link_usage = models.IntegerField(blank=True, null=True, default=0, verbose_name='Метрика посещений')
    slug = models.SlugField(blank=True, null=True)

    # price info
    price_for_promote = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default='0.15',
                                            verbose_name='Цена за продвижение')
    publish_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата публикации')

    votes = models.IntegerField('Голоса', default=0)
    votes_today = models.IntegerField('Голоса за сегодня', default=0)

    class Meta:
        ordering = ['-votes']

    def get_publish_date(self):
        return self.publish_date.strftime('%d.%m.%Y')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.coin_name)
        super(Coin, self).save(*args, **kwargs)

    def __str__(self):
        return self.coin_name

    def get_absolute_url(self):
        slug = slugify(self.coin_name)
        return reverse('core:coin-page', kwargs={'slug': slug})

    def format_number(self):
        try:
            number = float(self.market_cap)
        except:
            number = 0

        if number >= 1e9:  # Если число больше или равно 1 миллиарду
            result = '{:.2f}Billion'.format(number / 1e9)  # Делим число на 1 миллиард и добавляем букву 'B'
        elif number >= 1e6:  # Если число больше или равно 1 миллиону
            result = '{:.2f}Million'.format(number / 1e6)  # Делим число на 1 миллион и добавляем букву 'M'
        else:
            result = str(number)  # Если число меньше 1 миллиона, оставляем его без изменений

        return result

    def get_price(self):
        from core.utils import get_text_by_number

        if not self.price:
            return 0
        return get_text_by_number(self.price)

    def get_market_cap(self):
        from core.utils import get_text_by_number

        if not self.market_cap:
            return 0
        return get_text_by_number(self.market_cap)


@receiver(pre_save, sender=Coin)
def set_moderation_date(sender, instance, **kwargs):
    if instance.pk:  # Проверяем, что объект уже существует (редактирование)
        original_instance = sender.objects.get(pk=instance.pk)
        if original_instance.is_moderate != instance.is_moderate:
            if instance.is_moderate:
                current_time = datetime.now()
                instance.publish_date = current_time - timedelta(hours=3)
            else:
                instance.publish_date = None
    else:  # Создание нового объекта
        if instance.is_moderate:
            current_time = datetime.now()
            instance.publish_date = current_time - timedelta(hours=3)
        else:
            instance.publish_date = None


class Page(models.Model):
    title_seo = models.CharField(max_length=150, blank=True, null=True, verbose_name='Название для seo')
    description_seo = models.CharField(max_length=250, blank=True, null=True, verbose_name='Описание для seo')

    slug = models.SlugField(null=True, blank=True, )
    title = models.TextField(max_length=250, blank=True, default='', verbose_name='Заголовок')
    description = RichTextField(max_length=999999999999999, default='', blank=True, verbose_name='Описание')
    text_field_1 = RichTextField(max_length=999999999999999, default='', blank=True, verbose_name='Описание')
    text_field_3 = RichTextField(max_length=999999999999999, default='', blank=True, verbose_name='Описание')
    text_field_4 = RichTextField(max_length=999999999999999, default='', blank=True, verbose_name='Описание')


class Social(models.Model):
    title = models.CharField('Название', max_length=100)
    symbol = models.TextField('Символ (SVG)')
    url = models.CharField('Ссылка', max_length=255)
    sort = models.IntegerField('Сортировка', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Соц. сеть'
        verbose_name_plural = 'Соц. сети'
        ordering = ['sort']


class Cart(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_sum = models.DecimalField(max_digits=5, decimal_places=2, default='0.00', null=True, blank=True)

    def update_total_sum(self):
        order_items = OrderItem.objects.filter(cart=self)
        total_sum = Decimal(0)
        for order_item in order_items:
            if order_item.sum:
                total_sum += Decimal(order_item.sum)
        self.total_sum = total_sum
        self.save()

    def __str__(self):
        return f'Пользователь --- {self.user} | сумма заказа --- {self.total_sum} | id коризны {self.pk}'


class CartCold(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_sum = models.DecimalField(max_digits=5, decimal_places=2, default='0.00', null=True, blank=True)
    live_cart = models.IntegerField(null=True, blank=True)

    def update_total_sum(self):
        order_items = OrderItem.objects.filter(cart_cold=self)
        total_sum = Decimal(0)
        for order_item in order_items:
            if order_item.sum:
                total_sum += Decimal(order_item.sum)
        self.total_sum = total_sum
        self.save()


class CreateOrder(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    email = models.EmailField(blank=False, null=True, verbose_name='Почтовый ящик')
    cart_cold = models.ForeignKey('CartCold', on_delete=models.SET_NULL, null=True, related_name='orders', blank=True,
                                  verbose_name='Корзина пользователя')
    status = models.BooleanField(null=True, blank=True, verbose_name='Статус заказа')

    received = models.FloatField(default=0, null=True, blank=True, verbose_name='Отправленные')
    remaining = models.FloatField(default=0, null=True, blank=True, verbose_name='Полученные')

    def get_absolute_url(self):
        return reverse('order:order-lookup', kwargs={'pk': self.pk})

    def __str__(self):
        return f'Заказ {self.pk}, статус {self.status}'


class OrderItem(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Коин')
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    cart_cold = models.ForeignKey(CartCold, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Корзина')
    order_date = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name='Дата заказа рекламы')
    date = ArrayField(models.DateField(), null=True, verbose_name='Даты на которые заказли рекламу')
    type = models.CharField(null=True, blank=True, verbose_name='Тип рекламы')
    url = models.URLField(null=True, blank=True, verbose_name='Url для заказа с банером')
    photo = models.FileField(null=True, blank=True, verbose_name='Банер')
    sum = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Сумма')

    def update_sum(self, pk):
        order_items = OrderItem.objects.get(pk=self.pk)
        suma = 0
        suma += Decimal(order_items.coin.price_for_promote) * Decimal(len(order_items.date))
        self.sum = suma
        self.save()

    def get_absolute_url(self):
        return reverse('order:order-lookup',
                       kwargs={'pk': CreateOrder.objects.filter(cart_cold=self.cart_cold).first().pk})

    def __str__(self):
        try:
            return self.coin.coin_name
        except:
            return self.type


class AdvertisingItem(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя пользователя")
    email = models.EmailField(verbose_name="Email пользователя")
    question = models.TextField(verbose_name="Вопрос пользователя")

    def __str__(self):
        return f"Сообщение от {self.email}"


class Listing(models.Model):
    title = models.CharField('Название', max_length=100)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    filter_by = models.CharField('Фильтровать', max_length=100, default='all')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        super(Listing, self).save(*args, **kwargs)

    def get_first_coins(self):
        return self.get_coins()[:30]

    def get_coins(self):
        today = timezone.now().date()
        filter_by = self.filter_by
        if filter_by == 'all':
            coins = Coin.objects.filter(is_moderate=True)
        elif filter_by == 'promote':
            coins = Coin.objects.filter(promoted_status=True, is_moderate=True)
        elif filter_by == 'new':
            coins = Coin.objects.filter(is_moderate=True).order_by('-publish_date')
        elif filter_by == 'best_all':
            coins = Coin.objects.filter(is_moderate=True)
        elif filter_by == 'best_today':
            coins = Coin.objects.filter(is_moderate=True).exclude(votes_today=0).order_by('-votes_today')
        else:
            coins = Coin.objects.filter(is_moderate=True)
        return coins

    def get_sort_name(self):
        filter_by = self.filter_by
        sort = {
            'new': 'publish_date',
            'best_today': "votes_today",
        }
        if filter_by in sort.keys():
            return sort[filter_by]
        return 'votes'


class Setting(models.Model):
    url_for_banner = models.URLField(blank=True, null=True, verbose_name='Ссылка для банера на главной')
    photo_for_banner = models.FileField(blank=True, null=True, verbose_name='Фото для банера на главной')

    stat_title = models.CharField('Заголовок статистики (Главная)', max_length=150, blank=True)
    stat_text = models.TextField('Текст статистики (Главная)', blank=True)
    contacts_title = models.CharField('Заголовок контактов (Главная)', max_length=150, blank=True)
    copyright = models.CharField('Copyright', max_length=100, blank=True)
    footer_text = models.TextField('Текст футера', blank=True)

    promote_text = models.TextField('Текст (Promote)', blank=True)
    promote_text_spot = models.TextField('Текст (Promote Spot)', blank=True)
    promote_text_banner = models.TextField('Текст (Promote Banner)', blank=True)

    promote_stat_1 = models.IntegerField('(Promote Статистика) Пользователи', default=0)
    promote_stat_2 = models.IntegerField('(Promote Статистика) Twitter', default=0)
    promote_stat_3 = models.IntegerField('(Promote Статистика) Newsletter', default=0)

    total_currencies = models.IntegerField('(Статистика) Криптовалют', default=0)
    total_votes = models.IntegerField('(Статистика) Голосов', default=0)
    total_users = models.IntegerField('(Статистика) Пользователей', default=0)
    total_trading = models.IntegerField('(Статистика) Торговая стоимость', default=0)

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'

    @staticmethod
    def get_settings():
        settings = Setting.objects.all()
        if settings:
            return settings[0]
        else:
            settings = Setting()
            settings.save()
            return settings
