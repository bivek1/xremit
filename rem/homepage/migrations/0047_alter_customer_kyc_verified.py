# Generated by Django 4.2.2 on 2023-07-25 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0046_transaction_sending_purpose_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='kyc_verified',
            field=models.BooleanField(default=False),
        ),
    ]
