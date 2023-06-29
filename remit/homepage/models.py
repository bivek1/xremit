from django.db import models

# Create your models here.

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

# Create your models here.
class CustomUser(AbstractUser):
    user_type_data = (("owner", "owner"), ("agent", 'agent'), ("customer", 'customer'))
    user_type = models.CharField(default = "owner", choices = user_type_data, max_length = 20)
    email = models.EmailField(unique = True)
    
class Owner(models.Model):
    id = models.AutoField(primary_key = True)
    admin = models.OneToOneField(CustomUser, related_name ="owner", on_delete=models.CASCADE, null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.admin.first_name


class Agent(models.Model):
    id = models.AutoField(primary_key = True)
    admin = models.OneToOneField(CustomUser, related_name ="agent", on_delete=models.CASCADE, null = True, blank = True)
    number = models.BigIntegerField(null = True)
    mail_address = models.CharField(max_length=100, null = True, blank = True),
    state = models.CharField(max_length=100, null = True, blank = True),
    zip_code = models.IntegerField(null = True, blank = True),
    city = models.CharField(max_length=100, null = True, blank = True),
    country = models.CharField(max_length=100, null = True, blank = True),
    address = models.CharField(max_length = 200, null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add= True)
    profil_pic = models.ImageField(upload_to ="profile_pic/agent/", null = True, blank = True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(CustomUser, null=True, blank = True, related_name = 'agent_adder', on_delete = models.CASCADE)
    objects = models.Manager()
    
    def __str__(self):
        return self.admin.first_name

    
class Customer(models.Model):
    id = models.AutoField(primary_key = True)
    admin = models.OneToOneField(CustomUser, related_name ="customer", on_delete=models.CASCADE, null = True, blank = True)
    number = models.BigIntegerField(null = True)
    mail_address = models.CharField(max_length=100, null = True, blank = True)
    state = models.CharField(max_length=100, null = True, blank = True)
    zip_code = models.IntegerField(null = True, blank = True)
    city = models.CharField(max_length=100, null = True, blank = True)
    country = models.CharField(max_length=100, null = True, blank = True)
    address = models.CharField(max_length = 200, null = True, blank = True)
    profil_pic = models.ImageField(upload_to ="profile_pic/customer/", null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add= True)
    added_by = models.ForeignKey(CustomUser, null=True, blank = True, related_name = 'student_adder', on_delete = models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    enable_2fa = models.BooleanField(default=False)
    kyc_verified = models.BooleanField(default=False)
    objects = models.Manager()
    

    def __str__(self):
        return str(self.id)



class Country(models.Model):
    name = models.CharField(max_length=200)
    flag_img = models.ImageField(upload_to ="flag/", null = True, blank = True)
    allowed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

    
class PickupPoint(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, related_name='pickuppoint_country', on_delete=models.CASCADE)
    pickup_point = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Recipient(models.Model):
    # customer = models.ForeignKey(Customer, related_name='recipient_customer', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=300, choices=(
        ('CashPickup', 'Cash Pickup'),
        ('BankTransfer', 'Bank Transfer'),
        ('MobileTransfer', 'Mobile Transfer'),
        ('WallettoWalletTransfer', 'Wallet to Wallet Transfer')
    ))
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, related_name='recipent_country', on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=200, null = True, blank= True)
    city = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=200)
    number = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.first_name

class Currency(models.Model):
    country = models.ForeignKey(Country, related_name='currency_country', on_delete=models.CASCADE)
    currecy_rate = models.IntegerField()
    conversion_rate = models.IntegerField()
    commision_rate = models.IntegerField()
    currecy_sign = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.currecy_sign
    


class KYC(models.Model):
    customer = models.OneToOneField(Customer, related_name='kyc_customer', on_delete=models.CASCADE)
    country = models.ForeignKey(Country, related_name='kyc_country', on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=200, null = True, blank= True)
    city = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=200)
    number = models.BigIntegerField()
    gender = models.CharField(max_length=200, choices=(
        ('Male','Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ))
    document_type = models.CharField(max_length=200, choices=(
        ('Bank Account','Bank Account'),
        ('Benefits Card/ID', 'Benefits Card/ID'),
        ('Birth Certificate', 'Birth Certificate'),
        ('Business Registration/licence', 'Business Registration/licence'),
        ('Credit/debit card', 'Credit/debit card'),
        ('Driver licence', 'Driver licence'),
        ('Identity Card', 'Identity Card'),
        ('Passport', 'Passport'),
        ('Photo ID', 'Photo ID'),
        ('Security ID', 'Security ID'),
        ('Social Security ID', 'Social Security ID'),
        ('Student ID', 'Student ID'),
        ('Tax ID', 'Tax ID'),
        ('Other', 'Other'),
    ))
    document_front_image = models.ImageField(upload_to="document/")
    document_back_image = models.ImageField(upload_to="document/", null =True, blank = True)
    postal_address = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer.admin.usernamer






class TopHeader(models.Model):
    mail_address = models.CharField(max_length=200)
    support = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)



class CompanyInformation(models.Model):
    name = models.CharField(max_length=200, unique= True)
    short = models.CharField(max_length=300, unique= True, null = True, blank = True)
    aims = RichTextUploadingField()
    meta_description = models.CharField(max_length=1000, null = True, blank = True)
    logo = models.ImageField(upload_to = "logo/", null = True, blank = True)
    objects = models.Manager()

    def __str__(self):
        return self.name

class AboutUs(models.Model):
    about_us = RichTextUploadingField()
    objects = models.Manager()
    hide = models.BooleanField(default=False)

    def __str__(self):
        return self.about_us
    

class ChooseUs(models.Model):
    choose = RichTextUploadingField()
    objects = models.Manager()
    hide = models.BooleanField(default=False)

    def __str__(self):
        return self.choose
    

class HomeService(models.Model):
    service = RichTextUploadingField()
    image = models.ImageField(upload_to ="home_image/", blank = True, null = True)
    objects = models.Manager()
    hide = models.BooleanField(default=False)

    def __str__(self):
        return self.service
    
class SocialLink(models.Model):
    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=200)
    link = models.CharField(max_length=800)
    
    def __str__(self) -> str:
        return self.name


# Terms and Condition Model

class Terms(models.Model):
    terms = RichTextUploadingField()


    def __str__(self) -> str:
        return super().__str__()
    
# Policy Model

class Policy(models.Model):
    policy = RichTextUploadingField()


    def __str__(self) -> str:
        return super().__str__()
    


# Features
class Feature(models.Model):
    name = models.CharField(max_length=200)
    feature = RichTextUploadingField()


    def __str__(self) -> str:
        return super().__str__()

# Login and Sign Up interface page Model
class LoginInterface(models.Model):
    name = models.CharField(max_length=200)
    information = models.CharField(max_length=200)
    image = models.ImageField(upload_to='login_image/')
    
    def __str__(self) -> str:
        return self.name

class signupInterface(models.Model):
    name = models.CharField(max_length=200)
    information = models.CharField(max_length=200)
    image = models.ImageField(upload_to='signup_image/', null = True, blank=True)
    video = models.FileField(upload_to='signup_video/', null = True, blank=True)
    def __str__(self) -> str:
        return self.name

# Footor Information

class Footor(models.Model):
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=1000)
    
    def __str__(self) -> str:
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='login_image') 
    def __str__(self) -> str:
        return self.name
    

# Service
class Service(models.Model):
    name = models.CharField(max_length=300)
    description = RichTextUploadingField(null = True, blank = True)
    image = models.ImageField(upload_to = "services/", null = True, blank = True)

    objects = models.Manager()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=300)
    description = RichTextUploadingField(null = True, blank = True)
    image = models.ImageField(upload_to = "product/", null = True, blank = True)
    link = models.URLField(null = True, blank= True)
    objects = models.Manager()

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=300)
    description = RichTextUploadingField(null = True, blank = True)
    image = models.ImageField(upload_to = "services/", null = True, blank = True)
    link = models.URLField(null = True, blank= True)
    
    objects = models.Manager()

    def __str__(self):
        return self.name

class Testomonial(models.Model):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length = 300, null = True, blank = True)

    objects = models.Manager()

    def __str__(self):
        return self.name
    
# For Blogs and News Portal.............................................
class Category(models.Model):
    name = models.CharField(max_length= 200)
    objects = models.Manager()

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='category', on_delete=models.PROTECT)
    name = models.CharField(max_length=300)

    objects = models.Manager()

    def  __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=300)
    category = models.ForeignKey(Category, related_name  = "blog_category", on_delete = models.PROTECT, null = True, blank = True)
    sub_category = models.ForeignKey(SubCategory, related_name = "blog_sub_category", on_delete= models.PROTECT, null = True, blank = True)
    description = RichTextUploadingField()
    visit = models.IntegerField(null = True, blank = True)
    date_added = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now = True)
    objects = models.Manager()

    def __str__(self):
        return self.title
    


    

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "owner":
            Owner.objects.create(admin = instance)
        if instance.user_type == "agent":
            Agent.objects.create(admin = instance)
        if instance.user_type == "customer":
            Customer.objects.create(admin = instance)
       

@receiver(post_save, sender=CustomUser)
def post_save_receiver(sender, instance, **kwargs):
    if instance.user_type == "owner":
        instance.owner.save()
    if instance.user_type == "agent":
        instance.agent.save()
    if instance.user_type == "customer":
        instance.customer.save()
 
