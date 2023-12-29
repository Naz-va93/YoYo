# Generated by Django 4.2.1 on 2023-09-18 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_setting_copyright_setting_footer_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='copyright_en',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Copyright'),
        ),
        migrations.AddField(
            model_name='setting',
            name='copyright_ru',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Copyright'),
        ),
        migrations.AddField(
            model_name='setting',
            name='footer_text_en',
            field=models.TextField(blank=True, null=True, verbose_name='Текст футера'),
        ),
        migrations.AddField(
            model_name='setting',
            name='footer_text_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Текст футера'),
        ),
    ]
