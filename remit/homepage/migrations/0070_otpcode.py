# Generated by Django 4.2.2 on 2023-07-30 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0069_alter_screenshot_transaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTPcode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_otp', to='homepage.customer')),
            ],
        ),
    ]
