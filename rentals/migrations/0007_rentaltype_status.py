# Generated by Django 4.1 on 2022-10-11 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0006_rename_roomtype_rentaltype_alter_rentaltype_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentaltype',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
