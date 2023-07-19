# Generated by Django 4.2.2 on 2023-07-19 06:47

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0017_alter_defaultcurrency_currency'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EmailSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_host', models.CharField(max_length=200)),
                ('email_port', models.IntegerField()),
                ('email_host_user', models.CharField(max_length=200)),
                ('email_host_password', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SMSSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_sid', models.CharField(max_length=400)),
                ('auth_token', models.CharField(max_length=400)),
            ],
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='enable_2fa',
            new_name='banned',
        ),
        migrations.CreateModel(
            name='SMSList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to', models.BigIntegerField()),
                ('message', ckeditor_uploader.fields.RichTextUploadingField()),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sms_agent', to='homepage.recipient')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sms_customer', to='homepage.customer')),
                ('from_sim', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sending_number', to='homepage.defaultnumber')),
                ('reciptient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sms_recipient', to='homepage.recipient')),
            ],
        ),
        migrations.CreateModel(
            name='EmailList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('message', ckeditor_uploader.fields.RichTextUploadingField()),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent_email', to='homepage.agent')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_email', to='homepage.customer')),
                ('reciptient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='email_recipient', to='homepage.recipient')),
            ],
        ),
    ]
