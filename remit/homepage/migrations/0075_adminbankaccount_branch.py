# Generated by Django 4.2.2 on 2023-08-06 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0074_bankaccount_branch_transactionnote'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminbankaccount',
            name='branch',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
