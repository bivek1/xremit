# Generated by Django 4.2.2 on 2023-07-25 03:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0042_adminnotification_seen_customernotification_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminnotification',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='customer_admin_notification', to='homepage.customer'),
            preserve_default=False,
        ),
    ]
