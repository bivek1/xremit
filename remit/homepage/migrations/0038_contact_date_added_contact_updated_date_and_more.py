# Generated by Django 4.2.2 on 2023-07-23 08:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0037_alter_ticket_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
