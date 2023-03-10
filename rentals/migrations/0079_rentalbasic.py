# Generated by Django 4.1 on 2023-01-04 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0078_remove_rental_activities_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentalBasic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rental_type', models.CharField(max_length=100)),
                ('rental_basis', models.CharField(max_length=100)),
                ('floorspace', models.CharField(max_length=100)),
                ('floorspace_units', models.CharField(max_length=100)),
                ('grounds', models.CharField(max_length=100)),
                ('grounds_units', models.CharField(max_length=100)),
                ('floors_building', models.CharField(max_length=100)),
                ('entrance', models.CharField(max_length=100)),
                ('rental_licence', models.CharField(max_length=100)),
                ('user_id', models.IntegerField()),
                ('rental_id', models.IntegerField()),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'rental_basic',
            },
        ),
    ]
