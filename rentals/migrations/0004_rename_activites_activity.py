# Generated by Django 4.1 on 2022-10-11 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0003_activites_amenities'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Activites',
            new_name='Activity',
        ),
    ]
