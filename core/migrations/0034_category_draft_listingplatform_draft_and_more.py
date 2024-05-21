# Generated by Django 4.2.1 on 2024-05-21 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_alter_coin_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='draft',
            field=models.BooleanField(default=True, verbose_name='Черновик'),
        ),
        migrations.AddField(
            model_name='listingplatform',
            name='draft',
            field=models.BooleanField(default=True, verbose_name='Черновик'),
        ),
        migrations.AddField(
            model_name='networkchain',
            name='draft',
            field=models.BooleanField(default=True, verbose_name='Черновик'),
        ),
        migrations.AlterField(
            model_name='networkchain',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Фото'),
        ),
    ]
