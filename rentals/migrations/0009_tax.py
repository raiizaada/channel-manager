# Generated by Django 4.1 on 2022-10-13 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0008_rentaltype_created_at_rentaltype_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_name', models.CharField(max_length=100)),
                ('tax_percentage', models.CharField(max_length=20)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'tax',
            },
        ),
    ]