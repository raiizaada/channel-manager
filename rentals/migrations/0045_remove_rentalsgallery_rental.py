# Generated by Django 4.1 on 2022-12-08 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0044_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rentalsgallery',
            name='rental',
        ),
    ]
