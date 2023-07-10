# Generated by Django 4.2.2 on 2023-07-10 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0009_defaultcurrency'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='security',
            field=models.CharField(choices=[('email', 'email'), ('sms', 'sms'), ('both', 'both'), ('none', 'none')], default='none', max_length=200),
        ),
    ]