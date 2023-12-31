# Generated by Django 4.2.2 on 2023-07-29 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0062_alter_transaction_commision_rate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='commision_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='converting_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='fee',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='received',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='sent',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
