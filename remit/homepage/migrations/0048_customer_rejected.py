# Generated by Django 4.2.2 on 2023-07-25 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0047_alter_customer_kyc_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='rejected',
            field=models.BooleanField(default=False),
        ),
    ]
