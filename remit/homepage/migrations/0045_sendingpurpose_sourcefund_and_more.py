# Generated by Django 4.2.2 on 2023-07-25 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0044_transaction_created_at_transaction_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='SendingPurpose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='SourceFund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.AlterField(
            model_name='customer',
            name='kyc_verified',
            field=models.CharField(blank=True, choices=[('verified', 'Verified'), ('rejected', 'Rejected')], default='none', max_length=200, null=True),
        ),
    ]
