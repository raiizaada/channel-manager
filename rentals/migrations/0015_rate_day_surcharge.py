# Generated by Django 4.1 on 2022-10-14 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0014_remove_rate_channel_manager_markup'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='day_surcharge',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]