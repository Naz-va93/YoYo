# Generated by Django 4.2.1 on 2023-09-18 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_coin_listing_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='contacts_title',
            field=models.CharField(blank=True, max_length=150, verbose_name='Заголовок контактов (Главная)'),
        ),
        migrations.AddField(
            model_name='setting',
            name='contacts_title_en',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Заголовок контактов (Главная)'),
        ),
        migrations.AddField(
            model_name='setting',
            name='contacts_title_ru',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Заголовок контактов (Главная)'),
        ),
        migrations.AddField(
            model_name='setting',
            name='stat_text_en',
            field=models.TextField(blank=True, null=True, verbose_name='Текст статистики (Главная)'),
        ),
        migrations.AddField(
            model_name='setting',
            name='stat_text_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Текст статистики (Главная)'),
        ),
        migrations.AddField(
            model_name='setting',
            name='stat_title_en',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Заголовок статистики (Главная)'),
        ),
        migrations.AddField(
            model_name='setting',
            name='stat_title_ru',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Заголовок статистики (Главная)'),
        ),
    ]