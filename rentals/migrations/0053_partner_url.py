# Generated by Django 4.1 on 2022-12-09 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0052_remove_category_channel_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='url',
            field=models.TextField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
