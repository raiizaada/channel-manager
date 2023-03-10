# Generated by Django 4.1 on 2022-11-01 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0035_rentalamenities'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentalsGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='rentals-gallery')),
                ('user_id', models.IntegerField()),
                ('rental', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentals.rental')),
            ],
            options={
                'db_table': 'rentals_gallery',
            },
        ),
    ]
