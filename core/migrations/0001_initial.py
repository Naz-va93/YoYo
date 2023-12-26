# Generated by Django 4.2.1 on 2023-08-10 10:53

import ckeditor.fields
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('total_sum', models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=5, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartCold',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('total_sum', models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=5, null=True)),
                ('live_cart', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('name_en', models.CharField(max_length=100, null=True, verbose_name='Название')),
                ('name_ru', models.CharField(max_length=100, null=True, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_seo', models.CharField(blank=True, max_length=150, null=True, verbose_name='Название для seo')),
                ('description_seo', models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание для seo')),
                ('coin_name', models.CharField(max_length=50, verbose_name='Название')),
                ('coin_symbol', models.CharField(max_length=10, verbose_name='Абревиатура коина')),
                ('launch_date', models.DateField(null=True, verbose_name='Дата создания коина')),
                ('listing_link', models.URLField(verbose_name='Ссылка на листинг')),
                ('contact_address', models.CharField(max_length=100, verbose_name='Контактный адрес')),
                ('coin_description', models.TextField(max_length=1000, verbose_name='Описание коина')),
                ('coin_description_en', models.TextField(max_length=1000, null=True, verbose_name='Описание коина')),
                ('coin_description_ru', models.TextField(max_length=1000, null=True, verbose_name='Описание коина')),
                ('website_link', models.URLField()),
                ('twitter_link', models.URLField(blank=True)),
                ('telegram_link', models.URLField(blank=True)),
                ('discord_link', models.URLField(blank=True)),
                ('telegram_contact', models.CharField(max_length=250)),
                ('reddit_link', models.URLField(blank=True)),
                ('photo_coin', models.FileField(upload_to='', verbose_name='Фото')),
                ('binance_smart_chain', models.CharField(blank=True, null=True, verbose_name='Код chain')),
                ('market_cap', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Капитализация')),
                ('price', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Цена')),
                ('price_24h', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Цена за 24 часа')),
                ('is_api', models.BooleanField(null=True, verbose_name='Статус api')),
                ('promoted_status', models.BooleanField(default=False, null=True, verbose_name='Статус продвижения')),
                ('is_moderate', models.BooleanField(default=False, null=True, verbose_name='Статус модерации')),
                ('uuid', models.CharField(blank=True, null=True)),
                ('counter_link_usage', models.IntegerField(blank=True, default=0, null=True, verbose_name='Метрика посещений')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('price_for_promote', models.DecimalField(blank=True, decimal_places=2, default='0.15', max_digits=5, null=True, verbose_name='Цена за продвижение')),
                ('publish_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата публикации')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.category', verbose_name='Категория')),
                ('favorite', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ListingPlatform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('name_en', models.CharField(max_length=100, null=True, verbose_name='Название')),
                ('name_ru', models.CharField(max_length=100, null=True, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='NetworkChain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('name_en', models.CharField(max_length=100, null=True, verbose_name='Название')),
                ('name_ru', models.CharField(max_length=100, null=True, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, max_length=100, null=True)),
                ('photo', models.FileField(null=True, upload_to='', verbose_name='Фото')),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_seo', models.CharField(blank=True, max_length=150, null=True, verbose_name='Название для seo')),
                ('description_seo', models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание для seo')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('title', models.TextField(blank=True, max_length=250, null=True, verbose_name='Заголовок')),
                ('title_en', models.TextField(blank=True, max_length=250, null=True, verbose_name='Заголовок')),
                ('title_ru', models.TextField(blank=True, max_length=250, null=True, verbose_name='Заголовок')),
                ('description', ckeditor.fields.RichTextField(blank=True, max_length=999999999999999, null=True, verbose_name='Описание')),
                ('description_en', ckeditor.fields.RichTextField(blank=True, max_length=999999999999999, null=True, verbose_name='Описание')),
                ('description_ru', ckeditor.fields.RichTextField(blank=True, max_length=999999999999999, null=True, verbose_name='Описание')),
                ('text_field_1', ckeditor.fields.RichTextField(blank=True, max_length=999999999999999, null=True, verbose_name='Описание')),
                ('text_field_1_en', ckeditor.fields.RichTextField(blank=True, max_length=999999999999999, null=True, verbose_name='Описание')),
                ('text_field_1_ru', ckeditor.fields.RichTextField(blank=True, max_length=999999999999999, null=True, verbose_name='Описание')),
                ('text_field_2', ckeditor.fields.RichTextField(blank=True, max_length=999999999999999, null=True, verbose_name='Описание')),
                ('text_field_2_en', ckeditor.fields.RichTextField(blank=True, max_length=999999999999999, null=True, verbose_name='Описание')),
                ('text_field_2_ru', ckeditor.fields.RichTextField(blank=True, max_length=999999999999999, null=True, verbose_name='Описание')),
                ('text_field_3', ckeditor.fields.RichTextField(blank=True, max_length=999999999999999, null=True, verbose_name='Описание')),
                ('text_field_3_en', ckeditor.fields.RichTextField(blank=True, max_length=999999999999999, null=True, verbose_name='Описание')),
                ('text_field_3_ru', ckeditor.fields.RichTextField(blank=True, max_length=999999999999999, null=True, verbose_name='Описание')),
                ('text_field_4', ckeditor.fields.RichTextField(blank=True, max_length=999999999999999, null=True, verbose_name='Описание')),
                ('text_field_4_en', ckeditor.fields.RichTextField(blank=True, max_length=999999999999999, null=True, verbose_name='Описание')),
                ('text_field_4_ru', ckeditor.fields.RichTextField(blank=True, max_length=999999999999999, null=True, verbose_name='Описание')),
                ('text_field_5', models.TextField(blank=True, max_length=250, null=True, verbose_name='Описание')),
                ('text_field_5_en', models.TextField(blank=True, max_length=250, null=True, verbose_name='Описание')),
                ('text_field_5_ru', models.TextField(blank=True, max_length=250, null=True, verbose_name='Описание')),
                ('url_for_banner', models.URLField(blank=True, null=True, verbose_name='Ссылка для банера на главной')),
                ('photo_for_banner', models.FileField(blank=True, null=True, upload_to='', verbose_name='Фото для банера на главной')),
                ('score_1', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Показатель для цифр')),
                ('score_2', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Показатель для цифр')),
                ('score_3', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Показатель для цифр')),
                ('score_4', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Показатель для цифр')),
            ],
        ),
        migrations.CreateModel(
            name='Social',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('symbol', models.TextField(verbose_name='Символ (SVG)')),
                ('url', models.CharField(max_length=255, verbose_name='Ссылка')),
                ('sort', models.IntegerField(default=0, verbose_name='Сортировка')),
            ],
            options={
                'verbose_name': 'Соц. сеть',
                'verbose_name_plural': 'Соц. сети',
                'ordering': ['sort'],
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('name_en', models.CharField(max_length=100, null=True, verbose_name='Название')),
                ('name_ru', models.CharField(max_length=100, null=True, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.TimeField(auto_now_add=True, null=True)),
                ('date_new', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата голоса')),
                ('coin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.coin', verbose_name='Коин за который голосовали')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField(auto_now_add=True, null=True, verbose_name='Дата заказа рекламы')),
                ('date', django.contrib.postgres.fields.ArrayField(base_field=models.DateField(), null=True, size=None, verbose_name='Даты на которые заказли рекламу')),
                ('type', models.CharField(blank=True, null=True, verbose_name='Тип рекламы')),
                ('url', models.URLField(blank=True, null=True, verbose_name='Url для заказа с банером')),
                ('photo', models.FileField(blank=True, null=True, upload_to='', verbose_name='Банер')),
                ('sum', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Сумма')),
                ('cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.cart')),
                ('cart_cold', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.cartcold', verbose_name='Корзина')),
                ('coin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.coin', verbose_name='Коин')),
            ],
        ),
        migrations.CreateModel(
            name='CreateOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='Почтовый ящик')),
                ('status', models.BooleanField(blank=True, null=True, verbose_name='Статус заказа')),
                ('received', models.FloatField(blank=True, default=0, null=True, verbose_name='Отправленные')),
                ('remaining', models.FloatField(blank=True, default=0, null=True, verbose_name='Полученные')),
                ('cart_cold', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='core.cartcold', verbose_name='Корзина пользователя')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.AddField(
            model_name='coin',
            name='listing_platform',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.listingplatform', verbose_name='Платформа листинга'),
        ),
        migrations.AddField(
            model_name='coin',
            name='network_chain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.networkchain', verbose_name='Сеть'),
        ),
        migrations.AddField(
            model_name='coin',
            name='type_project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.type', verbose_name='Cетевая цепочка'),
        ),
    ]
