# Generated by Django 4.2.2 on 2023-07-23 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0035_ticket_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('answered', 'Answered'), ('closed', 'Closed')], default='pending', max_length=200),
        ),
    ]