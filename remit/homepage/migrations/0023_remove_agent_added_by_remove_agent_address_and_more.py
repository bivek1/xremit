# Generated by Django 4.2.2 on 2023-07-20 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0022_smslist_created_at_smslist_group_smslist_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agent',
            name='added_by',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='address',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='number',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='profil_pic',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='updated_at',
        ),
    ]
