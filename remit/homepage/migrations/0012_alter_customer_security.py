# Generated by Django 4.2.2 on 2023-07-12 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0011_footor_row'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='security',
            field=models.CharField(blank=True, choices=[('email', 'email'), ('sms', 'sms'), ('both', 'both'), ('none', 'none')], default='none', max_length=200, null=True),
        ),
    ]