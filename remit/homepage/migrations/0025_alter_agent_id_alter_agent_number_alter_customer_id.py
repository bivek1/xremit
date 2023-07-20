# Generated by Django 4.2.2 on 2023-07-20 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0024_agent_added_by_agent_address_agent_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='number',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
