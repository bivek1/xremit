# Generated by Django 4.2.2 on 2023-07-03 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_alter_recipient_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee', models.IntegerField()),
                ('converting_rate', models.IntegerField()),
                ('commision_rate', models.IntegerField(blank=True, null=True)),
                ('sent', models.IntegerField()),
                ('received', models.IntegerField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_transaction', to='homepage.customer')),
                ('receiving_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiving_currency', to='homepage.currency')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient_transaction', to='homepage.recipient')),
                ('sending_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sending_currency', to='homepage.currency')),
            ],
        ),
    ]