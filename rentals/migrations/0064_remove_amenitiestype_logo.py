# Generated by Django 4.1 on 2022-12-27 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0063_amenitiestype_remove_amenities_user_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amenitiestype',
            name='logo',
        ),
    ]
