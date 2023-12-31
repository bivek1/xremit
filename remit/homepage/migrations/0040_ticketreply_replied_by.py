# Generated by Django 4.2.2 on 2023-07-24 07:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0039_ticketreply'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketreply',
            name='replied_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_reply', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
