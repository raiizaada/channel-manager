# Generated by Django 4.1 on 2023-01-06 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0093_alter_rentaldeposit_security_deposit'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentalTax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_type', models.CharField(max_length=100)),
                ('fee_basis', models.CharField(max_length=100)),
                ('percentage', models.CharField(max_length=100)),
                ('amountin', models.CharField(max_length=100)),
                ('user_id', models.IntegerField()),
                ('rental_id', models.IntegerField()),
            ],
            options={
                'db_table': 'rental_tax',
            },
        ),
    ]
