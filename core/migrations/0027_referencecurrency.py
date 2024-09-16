# Generated by Django 4.2.1 on 2024-05-16 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_alter_coin_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferenceCurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=36, unique=True)),
                ('symbol', models.CharField(max_length=10)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('sign', models.CharField(blank=True, max_length=5, null=True)),
            ],
        ),
    ]