# Generated by Django 4.1 on 2022-10-29 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0030_companyprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='user_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
