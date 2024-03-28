# Generated by Django 4.2.1 on 2024-03-27 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_advertisingitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Порядок'),
        ),
    ]
