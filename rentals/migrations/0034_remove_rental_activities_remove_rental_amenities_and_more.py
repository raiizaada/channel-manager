# Generated by Django 4.1 on 2022-10-31 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0033_alter_rate_user_id_alter_ratetype_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rental',
            name='activities',
        ),
        migrations.RemoveField(
            model_name='rental',
            name='amenities',
        ),
        migrations.RemoveField(
            model_name='rental',
            name='policy',
        ),
    ]
