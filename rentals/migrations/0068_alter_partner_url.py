# Generated by Django 4.1 on 2022-12-28 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0067_rename_coutry_userprofile_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='url',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
