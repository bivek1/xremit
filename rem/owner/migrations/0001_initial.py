# Generated by Django 4.2.2 on 2023-06-27 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SEO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('meta_description', models.CharField(blank=True, max_length=1000, null=True)),
                ('meta_keywords', models.CharField(blank=True, max_length=1000, null=True)),
                ('canonical', models.CharField(blank=True, max_length=1000, null=True)),
                ('robot', models.CharField(blank=True, max_length=1000, null=True)),
                ('og_title', models.CharField(blank=True, max_length=1000, null=True)),
                ('og_description', models.CharField(blank=True, max_length=1000, null=True)),
                ('og_image', models.ImageField(blank=True, null=True, upload_to='og_image')),
            ],
        ),
        migrations.CreateModel(
            name='SiteSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(blank=True, max_length=300, null=True)),
                ('light_logo', models.ImageField(blank=True, null=True, upload_to='logo/')),
                ('dark_logo', models.ImageField(blank=True, null=True, upload_to='logo/')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='logo/')),
                ('email', models.CharField(blank=True, max_length=200, null=True)),
                ('number_one', models.BigIntegerField(blank=True, null=True)),
                ('number_two', models.BigIntegerField(blank=True, null=True)),
                ('address', models.CharField(max_length=200)),
            ],
        ),
    ]