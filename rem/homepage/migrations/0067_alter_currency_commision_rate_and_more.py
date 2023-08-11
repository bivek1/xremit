# Generated by Django 4.2.2 on 2023-07-29 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0066_remove_customer_zip_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='commision_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='currency',
            name='conversion_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='currency',
            name='currecy_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
