# Generated by Django 4.1 on 2022-12-25 22:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0057_subscription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='invoiceitem',
            name='user_id',
        ),
    ]
