from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class BlockPlace(models.Model):
    name = models.CharField(max_length=200)
    block = models.CharField(max_length=200, choices=(
        ('Country','Country'),
        ('Region', 'Region'),
        ('City', 'City')
    ))
    block_status = models.BooleanField(default=False)


    def __str__(self):
        return self.name



# Create your models here.
class SiteSetting(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, null=True, blank=True)
    light_logo = models.ImageField(upload_to='logo/', null=True, blank=True)
    dark_logo = models.ImageField(upload_to='logo/', null=True, blank=True)
    favicon = models.ImageField(upload_to='logo/', null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    number_one = models.BigIntegerField(null=True, blank=True)
    number_two = models.BigIntegerField(null=True, blank=True)
    address = models.CharField(max_length=200)

    def __str__(self):
        return str(self.title)

class SEO(models.Model):
    title = models.CharField(max_length=200)
    meta_description = models.CharField(max_length=1000, null=True, blank=True)
    meta_keywords = models.CharField(max_length=1000, null=True, blank=True)
    canonical = models.CharField(max_length=1000, null=True, blank=True)
    robot = models.CharField(max_length=1000, null=True, blank=True)
    og_title = models.CharField(max_length=1000, null=True, blank=True)
    og_description = models.CharField(max_length=1000, null=True, blank=True)
    og_image = models.ImageField(upload_to='og_image', null=True, blank=True)
   
    def __str__(self):
        return str(self.title)
    

    


