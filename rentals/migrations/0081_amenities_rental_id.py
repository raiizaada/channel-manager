# Generated by Django 4.1 on 2023-01-04 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0080_rentallocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='amenities',
            name='rental_id',
            field=models.IntegerField(null=True),
        ),
    ]
