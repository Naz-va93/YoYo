# Generated by Django 4.2.1 on 2023-09-18 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_setting_contacts_title_setting_contacts_title_en_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='copyright',
            field=models.CharField(blank=True, max_length=100, verbose_name='Copyright'),
        ),
        migrations.AddField(
            model_name='setting',
            name='footer_text',
            field=models.TextField(blank=True, verbose_name='Текст футера'),
        ),
    ]
