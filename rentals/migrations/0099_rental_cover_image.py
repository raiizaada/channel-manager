# Generated by Django 4.1 on 2023-01-06 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0098_alter_channel_channel_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='rental',
            name='cover_image',
            field=models.ImageField(default=None, null=True, upload_to='rentals'),
        ),
    ]
