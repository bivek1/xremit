# Generated by Django 4.2.2 on 2023-07-17 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0012_alter_customer_security'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kyc',
            name='document_type',
            field=models.CharField(choices=[('Business Registration/licence', 'Business Registration/licence'), ('Driver licence', 'Driver licence'), ('Passport', 'Passport')], max_length=200),
        ),
    ]