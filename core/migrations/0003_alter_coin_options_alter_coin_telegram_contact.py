# Generated by Django 4.2.1 on 2023-09-04 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coin',
            options={'ordering': ['-votes']},
        ),
        migrations.AlterField(
            model_name='coin',
            name='telegram_contact',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
