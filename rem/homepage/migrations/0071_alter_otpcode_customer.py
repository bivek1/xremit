# Generated by Django 4.2.2 on 2023-07-30 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0070_otpcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpcode',
            name='customer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_otp', to='homepage.customer'),
        ),
    ]