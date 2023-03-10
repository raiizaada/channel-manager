# Generated by Django 4.1 on 2022-11-02 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0038_remove_rentalamenities_amenities_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rental',
            name='activities_id',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rental',
            name='amenities_id',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rental',
            name='policy_id',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='RentalAmenities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('amenities', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentals.amenities')),
                ('rental', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentals.rental')),
            ],
            options={
                'db_table': 'rental_amenities',
            },
        ),
    ]
