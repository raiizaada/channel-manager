# Generated by Django 4.1 on 2022-10-18 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0023_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rental_name', models.CharField(max_length=20)),
                ('rental_logo', models.ImageField(upload_to='rentals')),
                ('rental_url', models.CharField(max_length=100)),
                ('rental_description', models.TextField(max_length=1000)),
                ('activities', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentals.activity')),
                ('amenities', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentals.amenities')),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentals.policy')),
            ],
            options={
                'db_table': 'rental',
            },
        ),
    ]
