# Generated by Django 4.2.1 on 2024-04-27 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_coin_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='coin',
            name='all_time_high',
            field=models.FloatField(blank=True, default=0.0, null=True, verbose_name='Все время высокий'),
        ),
        migrations.AddField(
            model_name='coin',
            name='all_time_high_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата всех времен высокий'),
        ),
        migrations.AddField(
            model_name='coin',
            name='fully_diluted_market_cap',
            field=models.FloatField(blank=True, default=0.0, null=True, verbose_name='Полностью разбавленная капитализация'),
        ),
        migrations.AddField(
            model_name='coin',
            name='volume_24h',
            field=models.FloatField(blank=True, default=0.0, null=True, verbose_name='Объем за 24 часа'),
        ),
    ]
