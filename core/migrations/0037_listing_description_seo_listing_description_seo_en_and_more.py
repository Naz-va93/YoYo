# Generated by Django 4.2.1 on 2024-10-11 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_listing_title_seo_listing_title_seo_en_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='description_seo',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание для seo'),
        ),
        migrations.AddField(
            model_name='listing',
            name='description_seo_en',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание для seo'),
        ),
        migrations.AddField(
            model_name='listing',
            name='description_seo_ru',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание для seo'),
        ),
    ]
