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


class Country(models.Model):
    name = models.CharField(max_length=200)
    flag_img = models.ImageField(upload_to ="flag/", null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Agent(models.Model):

    admin = models.OneToOneField(CustomUser, related_name ="agent", on_delete=models.CASCADE, null = True, blank = True)
    mail_address = models.CharField(max_length=100, null = True, blank = True)
    state = models.CharField(max_length=100, null = True, blank = True)
    zip_code = models.IntegerField(null = True, blank = True)
    city = models.CharField(max_length=100, null = True, blank = True)
    country = models.ForeignKey(Country, related_name='agent_country', on_delete=models.CASCADE, null = True, blank= True)
    address = models.CharField(max_length = 200, null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add= True)
    profil_pic = models.ImageField(upload_to ="profile_pic/agent/", null = True, blank = True)
    number = models.BigIntegerField(null = True, blank = True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(CustomUser, null=True, blank = True, related_name = 'agent_adder', on_delete = models.CASCADE)
    objects = models.Manager()
    
    def __str__(self):
        try:
            return self.admin.first_name
        except:
            return str(self.id)


    
class Customer(models.Model):
 
    admin = models.OneToOneField(CustomUser, related_name ="customer", on_delete=models.CASCADE, null = True, blank = True)
    number = models.BigIntegerField(null = True)
    mail_address = models.CharField(max_length=100, null = True, blank = True)
    state = models.CharField(max_length=100, null = True, blank = True)
    city = models.CharField(max_length=100, null = True, blank = True)
    country = models.CharField(max_length=100, null = True, blank = True)
    address = models.CharField(max_length = 200, null = True, blank = True)
    profil_pic = models.ImageField(upload_to ="profile_pic/customer/", null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add= True)
    added_by = models.ForeignKey(CustomUser, null=True, blank = True, related_name = 'student_adder', on_delete = models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    banned = models.BooleanField(default=False)
    security = models.CharField(max_length=200, choices=(
        ('email', 'email'),
        ('sms', 'sms'),
        ('both', 'both'),
        ('none','none')
    ), default='none', null= True, blank = True)
    kyc_verified = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    
    objects = models.Manager()
    

    def __str__(self):
        try:
            return self.admin.first_name
        except:
            return str(self.id)


class SendingPurpose(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name
    
class SourceFund(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class OTPcode(models.Model):
    customer = models.OneToOneField(Customer, related_name='customer_otp',on_delete=models.CASCADE, null= True, blank= True)
    code = models.IntegerField()

    def __str__(self):
        return str(self.code)
    
class Restriction(models.Model):
    minimum_amount = models.IntegerField()
    maximum_amount = models.IntegerField()
    daily_transfer_remit = models.IntegerField()
    maximum_cap_charge = models.IntegerField()

    def __str__(self):
        return str(self.maximum_amount)
    
class EmailSetting(models.Model):
    email_host = models.CharField(max_length=200)
    email_port = models.IntegerField()
    email_host_user = models.CharField(max_length=200)
    email_host_password = models.CharField(max_length=200)

    def __str__(self):
        return self.email_host



class DefaultNumber(models.Model):
    number = models.BigIntegerField()

    def  __str__(self):
        return str(self.number)

class SMSSetting(models.Model):
    account_sid  = models.CharField(max_length=400)
    auth_token  = models.CharField(max_length=400)
   
  

    def __str__(self):
        return str(self.account_sid)
    



 
class PickupPoint(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, related_name='pickuppoint_country', on_delete=models.CASCADE)
    pickup_point = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Recipient(models.Model):
    customer = models.ForeignKey(Customer, related_name='recipient_customer', on_delete=models.CASCADE, null = True, blank=True)
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
    

class SMSList(models.Model):
    customer = models.ForeignKey(Customer, related_name='sms_customer', on_delete=models.DO_NOTHING, null = True, blank= True)
    reciptient = models.ForeignKey(Recipient, related_name='sms_recipient', on_delete=models.DO_NOTHING, null = True, blank= True)
    agent = models.ForeignKey(Recipient, related_name='sms_agent', on_delete=models.DO_NOTHING, null = True, blank= True)
    to = models.BigIntegerField(null = True, blank=True)
    message = models.TextField()
    group = models.CharField(max_length=200, choices=(
        ('Agent', 'Agent'),
        ('Customer', 'Customer'),
        ('Recipient', 'Recipient'),
        ('All', 'All'),
        ('Individual', 'Individual')
    ), default= 'Individual')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.subject
    

class EmailList(models.Model):
    customer = models.ForeignKey(Customer, related_name='customer_email', on_delete=models.CASCADE, null = True, blank=True)
    reciptient = models.ForeignKey(Recipient, related_name='email_recipient', on_delete=models.DO_NOTHING, null = True, blank= True)
    agent = models.ForeignKey(Agent, related_name='agent_email', on_delete=models.CASCADE, null = True, blank=True)
    subject = models.CharField(max_length=200)
    message = RichTextUploadingField()
    group = models.CharField(max_length=200, choices=(
        ('Agent', 'Agent'),
        ('Customer', 'Customer'),
        ('Recipient', 'Recipient'),
        ('All', 'All'),
        ('Individual', 'Individual')
    ), default= 'Individual')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.subject
    

class Currency(models.Model):
    country = models.OneToOneField(Country, related_name='currency_country', on_delete=models.CASCADE)
    currecy_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    conversion_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commision_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currecy_sign = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.currecy_sign
    
class DefaultCurrency(models.Model):
    customer = models.OneToOneField(Customer, related_name='customer_currency', on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, related_name='default_currency', on_delete=models.CASCADE)

    def __str__(self):
        return self.customer.admin.get_full_name()
    

class DefaultCurrencyAdmin(models.Model):
    sending_currency = models.ForeignKey(Currency, related_name='default_sending_currency', on_delete=models.CASCADE)
    receiving_currency = models.ForeignKey(Currency, related_name='default_receiving_currency', on_delete=models.CASCADE)
    

    def __str__(self):
        return self.sending_currency.currecy_sign
    
class BankAccount(models.Model):
    customer = models.ForeignKey(Customer, related_name='customer_bank', on_delete=models.CASCADE)
    recipient = models.ForeignKey(Recipient, related_name='recipient_bank', on_delete=models.CASCADE)
    account_name = models.CharField(max_length=300)
    branch = models.CharField(max_length=200)
    account_number = models.CharField(max_length=500)
    bank_name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, related_name='country_bank', on_delete=models.CASCADE)
    swift_code = models.CharField(max_length=200)

    def __str__(self):
        return self.recipient.first_name
    
class AdminBankAccount(models.Model):
    account_name = models.CharField(max_length=300)
    account_number = models.CharField(max_length=500)
    branch = models.CharField(max_length=200)
    bank_name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, related_name='admin_country_bank', on_delete=models.CASCADE)
    swift_code = models.CharField(max_length=200)

    def __str__(self):
        return self.account_name

class Transaction(models.Model):
    customer = models.ForeignKey(Customer, related_name='customer_transaction', on_delete=models.CASCADE)
    recipient = models.ForeignKey(Recipient, related_name='recipient_transaction', on_delete=models.CASCADE)
    sending_currency = models.ForeignKey(Currency, related_name='sending_currency', on_delete=models.CASCADE)
    receiving_currency = models.ForeignKey(Currency, related_name='receiving_currency', on_delete=models.CASCADE)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    converting_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commision_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    received = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sent_money_to_us = models.BooleanField(default=False)
    sent_to_client = models.BooleanField(default=False)
    status = models.CharField(max_length= 200, choices=(
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Rejected', 'Rejected')
    ), default='Pending')
    bank = models.ForeignKey(BankAccount, related_name='transaction_bank', null = True, blank= True, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
    sending_purpose = models.ForeignKey(SendingPurpose, related_name = "transaction_purpose", on_delete=models.DO_NOTHING, null = True, blank= True)
    source_of_fund = models.ForeignKey(SourceFund, related_name = "transaction_source", on_delete=models.DO_NOTHING, null = True, blank= True)
    
    def __str__(self):
        return self.customer.admin.get_full_name()


    def count_total(self):
        ss = Transaction.objects.filter(customer = self.customer).count()
        return ss


class TransactionNote(models.Model):
    transaction = models.ForeignKey(Transaction, related_name='transaction_note' ,on_delete=models.CASCADE)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.note

class ScreenShot(models.Model):
    transaction = models.OneToOneField(Transaction, related_name='transaction_screenshot' ,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='screenshot/')

class KYC(models.Model):
    image = models.ImageField(upload_to='kyc_image', null = True, blank=True)
    customer = models.ForeignKey(Customer, related_name='kyc_customer', on_delete=models.CASCADE, null = True, blank=True)
    country = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=200, null = True, blank= True)
    city = models.CharField(max_length=200)
    number = models.BigIntegerField()
    postal_address = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=200, choices=(
        ('Male','Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ))
    document_type = models.CharField(max_length=200, choices=(
        ('National ID', 'National ID'),
        ('Driver licence', 'Driver licence'),
        ('Passport', 'Passport'),
    ))
    


    # Licence
    licence_number = models.IntegerField(null = True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    document_front_image = models.ImageField(upload_to="document/", null =True, blank = True)
    document_back_image = models.ImageField(upload_to="document/", null =True, blank = True)
    

    # Passport
    passport_number = models.IntegerField(null = True, blank=True)
    passport_issue_date = models.DateField(null=True, blank=True)
    passport_expiry_date = models.DateField(null=True, blank=True)
    passport_image = models.ImageField(upload_to="document/", null =True, blank = True)
    passport_issued_country = models.CharField(max_length=200, null =True, blank = True)
    # passport_image = models.ImageField(upload_to="document/", null =True, blank = True)

    # Business Registration 
    business_image = models.ImageField(upload_to='document/', null =True, blank = True)
    business_registration_date = models.DateField(null = True, blank=True)
    registraion_number = models.IntegerField(null = True, blank=True)
    
    

    
   
    
    
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.customer.admin.username



# class LicenceDetail(models.Model):
#     kyc = models.OneToOneField(KYC, related_name='kyc_document', on_delete=models.CASCADE)
#     document_front_image = models.ImageField(upload_to="document/")
#     document_back_image = models.ImageField(upload_to="document/", null =True, blank = True)
#     issue_date = models.DateField(null=True, blank=True)
#     expiry_date = models.DateField(null=True, blank=True)

    
#     def __str__(self):
#         return str(self.kyc.customer.number)
    
# class RegistrationDetail(models.Model):
#     kyc = models.OneToOneField(KYC, related_name='kyc_document', on_delete=models.CASCADE)
#     document_front_image = models.ImageField(upload_to="document/")
#     document_back_image = models.ImageField(upload_to="document/", null =True, blank = True)
#     issue_date = models.DateField(null=True, blank=True)
#     expiry_date = models.DateField(null=True, blank=True)

    
    def __str__(self):
        return str(self.kyc.customer.number)


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
    image = models.ImageField(upload_to ="features_image/", blank = True, null = True)
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
    row = models.CharField(max_length=100, choices=(
        ('First', 'First'),
        ('Second', 'Second'),
        ('Third', 'Third')
    ), default="First")
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
    image = models.ImageField(upload_to = "blogs/", null = True, blank = True)
    types = models.CharField(max_length=200, choices=(
        ('News', 'News'),
        ('Blog', 'Blog')
    ))
  
    description = RichTextUploadingField()
    visit = models.IntegerField(null = True, blank = True)
    date_added = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now = True)
    objects = models.Manager()

    def __str__(self):
        return self.title
    

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(null = True, blank=True)
    number = models.BigIntegerField()
    message = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now = True)
   
    def __str__(self):
        return self.name

class Ticket(models.Model):
    customer = models.ForeignKey(Customer, related_name='customer_support', on_delete=models.CASCADE)
    department = models.CharField(max_length=200, choices=(
        ('technical','Technical'),
        ('payment', 'Payment'),
    ))
    piority = models.CharField(max_length=200, choices=(
        ('high','High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ))
    status = models.CharField(max_length=200, choices=(
        ('pending','Pending'),
        ('answered', 'Answered'),
        ('closed', 'Closed')
    ), null = True, blank = True)
    subject = models.CharField(max_length=300)
    description = RichTextUploadingField()
    date_added = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.subject
    
class TicketReply(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='ticket_reply', on_delete=models.CASCADE, null = True, blank=True)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now = True)
    replied_by = models.ForeignKey(CustomUser, related_name='user_reply', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.ticket.subject
    
class AdminNotification(models.Model):
    name = models.CharField(max_length=300)
    customer = models.ForeignKey(Customer, related_name='customer_admin_notification', on_delete=models.CASCADE) 
    types = models.CharField(max_length=200, choices=(
        ('transaction','transaction'),
        ('kyc', 'kyc'),
        ('user', 'user'),
        ('ticket', 'ticket'),
    ), null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    ids = models.IntegerField(null = True, blank=True)
    seen = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class CustomerNotification(models.Model):
    customer = models.ForeignKey(Customer, related_name='customer_notification', on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    types = models.CharField(max_length=200, choices=(
        ('transaction','transaction'),
        ('kyc', 'kyc'),
        ('ticket', 'ticket'),
    ), null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    ids = models.IntegerField(null = True, blank=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class SupportFile(models.Model):
    file = models.FileField(upload_to='support_file/')
    support = models.ForeignKey(Ticket, related_name='customer_support', on_delete=models.CASCADE)

    def __str__(self):
        return self.support.subject

class LoginLogs(models.Model):
    customer = models.ForeignKey(Customer, related_name='customer_logs', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_aadress = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    
    def __str__(self):
        return self.customer.admin.username
    

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
 
