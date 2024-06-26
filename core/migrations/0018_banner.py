# Generated by Django 4.2.1 on 2024-04-17 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='banners/', verbose_name='Фото')),
                ('location', models.CharField(choices=[('index_under_header', 'На главной странице, под шапкой')], default='index_under_header', max_length=50, verbose_name='Расположение')),
                ('url', models.URLField(max_length=250, verbose_name='Ссылка')),
                ('show', models.BooleanField(default=True, verbose_name='Показ')),
            ],
        ),
    ]
