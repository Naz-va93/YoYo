# Generated by Django 4.2.1 on 2024-03-28 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_category_options_category_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='networkchain',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='networkchain',
            name='order',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Порядок'),
        ),
    ]
