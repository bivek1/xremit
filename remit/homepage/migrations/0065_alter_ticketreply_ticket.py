# Generated by Django 4.2.2 on 2023-07-29 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0064_alter_currency_commision_rate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketreply',
            name='ticket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ticket_reply', to='homepage.ticket'),
        ),
    ]
