# Generated by Django 4.2.1 on 2024-10-08 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_coin_description_seo_en_coin_description_seo_ru_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='title_seo',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Название для seo'),
        ),
        migrations.AddField(
            model_name='listing',
            name='title_seo_en',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Название для seo'),
        ),
        migrations.AddField(
            model_name='listing',
            name='title_seo_ru',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Название для seo'),
        ),
        migrations.AddField(
            model_name='page',
            name='description_seo_en',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание для seo'),
        ),
        migrations.AddField(
            model_name='page',
            name='description_seo_ru',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание для seo'),
        ),
        migrations.AddField(
            model_name='page',
            name='title_seo_en',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Название для seo'),
        ),
        migrations.AddField(
            model_name='page',
            name='title_seo_ru',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Название для seo'),
        ),
    ]