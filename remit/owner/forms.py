from django import forms
from homepage.models import Feature, AboutUs, ChooseUs, HomeService, Brand ,LoginInterface, signupInterface, Policy, Footor, Service, Client, Testomonial, Terms, SocialLink, TopHeader, CompanyInformation
from .models import SiteSetting, SEO
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from homepage.models import Currency, Country, Recipient, PickupPoint, KYC, EmailSetting, SMSSetting, EmailList, SMSList, DefaultNumber
from homepage.models import SendingPurpose, SourceFund
from .models import BlockPlace

# Block Place Form
class BlockForm(forms.ModelForm):
    class Meta:
        model = BlockPlace
        fields = ('__all__')

        widgets={
            'name': forms.TextInput(attrs = {'class':'form-control mt-2', 'placeholder':'Name of the place..'}),
            'block':forms.Select(attrs = {'class':'form-control mt-2'})
        }



# Sending purpose and fund setting
class PurposeForm(forms.ModelForm):
    class Meta:
        model = SendingPurpose
        fields = ('__all__')

        widgets={
            'name': forms.TextInput(attrs = {'class':'form-control mt-2', 'placeholder':'Name of the sending purpose..'})
        }


class FundForm(forms.ModelForm):
    class Meta:
        model = SourceFund
        fields = ('__all__')

        widgets={
            'name': forms.TextInput(attrs = {'class':'form-control mt-2', 'placeholder':'Name of the source fund..'})
        }


# EMAIL AND SMS SETTINGS
class EmailSettingForm(forms.ModelForm):
    class Meta:
        model = EmailSetting
        fields = ('__all__')

        widgets = {
            'email_host':forms.TextInput(attrs = {'class':'form-control','placeholder':'mail.xremit.com'}),
            'email_port':forms.TextInput(attrs = {'class':'form-control','placeholder':'465'}),
            'email_host_user':forms.TextInput(attrs = {'class':'form-control','placeholder':'info@xremit.com'}),
            'email_host_password':forms.TextInput(attrs = {'class':'form-control','placeholder':'*******', 'type':'password'}),
        }

class DefaultForm(forms.ModelForm):
    class Meta:
        model = DefaultNumber
        fields = ('__all__')

        widgets={
            'number': forms.NumberInput(attrs = {'class':'form-control mt-2', 'placeholder':'Enter your twilo phone number'})
        }

class EmailListForm(forms.ModelForm):
    class Meta:
        model = EmailList
        fields = ("subject", 'message','customer', 'reciptient', 'agent', 'group')

        widgets = {
            'subject':forms.TextInput(attrs = {'class':'form-control','placeholder':'Subject of your email'}),
            'customer':forms.TextInput(attrs = {'class':'form-control','hidden':True}),
            'reciptient':forms.TextInput(attrs = {'class':'form-control','hidden':True}),
            'group':forms.Select(attrs = {'class':'form-control','hidden':True}),
            'agent':forms.TextInput(attrs = {'class':'form-control','hidden':True}),
            'message':CKEditorUploadingWidget()
        }


class SMSSettingForm(forms.ModelForm):
    class Meta:
        model = SMSSetting
        fields = ('__all__')

        widgets = {
            'account_sid':forms.TextInput(attrs = {'class':'form-control mt-2','placeholder':'Account id'}),
            'auth_token':forms.TextInput(attrs = {'class':'form-control mt-2','placeholder':'authentication token'}),
        }


class SMSListForm(forms.ModelForm):
    class Meta:
        model = SMSList
        fields = ("from_sim", 'to' , 'message', 'reciptient', 'agent', 'group', 'customer')

        widgets = {
            'from_sim':forms.Select(attrs = {'class':'form-control'}),
            'to':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'+61782782'}),
            'reciptient':forms.Select(attrs={'hidden':True}),
            'agent':forms.Select(attrs={'hidden':True}),
            'group':forms.Select(attrs={'hidden':True}),
            'customer':forms.Select(attrs={'hidden':True}),
            'message':CKEditorUploadingWidget()
        }
# KYCForm
class KYCForm(forms.ModelForm): 
    class Meta:
        model = KYC
        fields = ('__all__')


        widgets= {
            'image':forms.FileInput(attrs={'accept':"image/*", 'class':'form-control  custom-input mt-2', 'id':'image-upload' ,'onchange':"showImage(this)", 'required':False}),
            'country':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Australia' }),
            'address':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'123 Smith Street, Richmond, Victoria'}),
            'state':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Victoria'}),
            'city':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Melbourne'}),
            'postal_address':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'14428. Melbourne, VIC 8001'}),
            'number':forms.NumberInput(attrs={'class':'form-control mt-2', 'placeholder':'+61 4 91 575 789'}),
            'gender':forms.Select(attrs={'class':'form-control mt-2'}),
            'document_type':forms.Select(attrs={'class':'form-control mt-2', 'hidden':True}),
            'date_of_birth':forms.DateInput(attrs={'type':'date','class':'form-control mt-2'}),
            
            # Licence
            'licence_number':forms.NumberInput(attrs={'class':'form-control mt-2', 'placeholder':'01245422354','value':'{{cm.licence_number}}'}),
            'document_front_image':forms.FileInput(attrs={'accept':"image/*", 'class':'form-control mt-2','onchange':"showFrontImage(this);"}),
            'document_back_image':forms.FileInput(attrs={'accept':"image/*", 'class':'form-control mt-2','onchange':"showBackImage(this);"}),
            'issue_date' : forms.DateInput(attrs={'type':'date','class':'form-control mt-2','value':'{{cm.issue_date}}'}),
            'expiry_date' : forms.DateInput(attrs={'type':'date','class':'form-control mt-2','value':'{{cm.expiry_date}}'}),   
            
            # Passport
           
            'passport_number':forms.NumberInput(attrs={'class':'form-control mt-2', 'placeholder':'01245422354','value':'{{cm.passport_number}}'}),
            'passport_image':forms.FileInput(attrs={'accept':"image/*", 'class':'form-control mt-2','onchange':"showPassportImage(this);"}),
            'passport_issue_date' : forms.DateInput(attrs={'type':'date','class':'form-control mt-2','value':'{{cm.issue_date}}'}),
            'passport_expiry_date' : forms.DateInput(attrs={'type':'date','class':'form-control mt-2','value':'{{cm.expiry_date}}'}),   
            'passport_issued_country': forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Australia', 'value:':'{%if cm.passport_issued_country%}{{cm.passport_issued_country}}{%endif%}'}),
            
        
           
            # Registration
            'business_image':forms.FileInput(attrs={'accept':"image/*", 'class':'form-control mt-2','onchange':"showBusinessImage(this);"}),
            'business_registration_date' : forms.DateInput(attrs={'type':'date', 'class':'form-control mt-2','value':'{{cm.business_registration_date}}'}),
            'registraion_number': forms.NumberInput(attrs={'class':'form-control mt-2', 'placeholder':'01245422354','value':'{{cm.registraion_number}}'}),
        }


# PickupPointForm

class PickupPointForm(forms.ModelForm):
    class Meta:
        model = PickupPoint
        fields = ('__all__')

        widgets= {
            'name':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Name of the Pickup Point'}),
            'country':forms.Select(attrs={'class':'form-control mt-2'}),
            'pickup_point':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Address of Pickup Point'}),
            
        }



# RecipientForm
class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ('__all__')

        widgets= {
            'transaction_type':forms.Select(attrs={'class':'form-control mt-2'}),
            'first_name':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'First Name'}),
            'middle_name':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Middle Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Last Name'}),
            'city':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Melbourne'}),
            'zip_code':forms.NumberInput(attrs={'class':'form-control mt-2', 'placeholder':'30001'}),
            'number':forms.NumberInput(attrs={'class':'form-control mt-2', 'placeholder':'+61 4 91 575 789'}),
            'country':forms.Select(attrs={'class':'form-control mt-2', 'placeholder':'Australia'}), 
            'address':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'123 Smith Street, Richmond, Victoria'}),
            'state':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Victoria'}),  
        }



# CountryForm

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ('__all__')

        widgets= {
            'name':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Nepal'}),
            'flag_img':forms.FileInput(attrs={'accept':"image/*", 'class':'form-control mt-2'}),
            'allowed':forms.Select(attrs={'class':'form-control mt-2'}),
        }


# CurrencyForm
class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = ('__all__')

        labels={
            'country': 'Select the country*',
            'currecy_rate':'Write Currency rate in rate unit of USD i.e. 1USD = 1.50 AUD*',
            'conversion_rate':'Enter the your conversion service rate*',
            'commision_rate':'Enter agent commision rate if any',
            'currecy_sign':'Enter the currecy sign of Country i.e. AUD for Australia*'
        }
        widgets= {
            'country':forms.Select(attrs={'class':'form-control mt-2'}),
            'currecy_rate':forms.NumberInput(attrs={'step':'any','class':'form-control mt-2','placeholder':'1.5 AUD in USD unit'}),
            'conversion_rate':forms.NumberInput(attrs={'step':'any','class':'form-control mt-2', 'placeholder':'Your conversion rate of selected country currency'}),
            'commision_rate':forms.NumberInput(attrs={'step':'any',' class':'form-control mt-2', 'placeholder':'Your commsion rate for agent of selected country currency'}),
            'currecy_sign':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Sign of selected country currency: NPR, AUD, USD'}),
        }




# Above new currency and payment related plus, verificaton
# Bellow Site forms

class SiteForm(forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = ('__all__')

        widgets= {
            'title':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Title of the site'}),
            'subtitle':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Sub title of the site'}),
            'light_logo':forms.FileInput(attrs={'accept':"image/*",'class':'form-control mt-2', 'placeholder':'Title of the site'}),
            'dark_logo ':forms.FileInput(attrs={'accept':"image/*", 'class':'form-control mt-2', 'placeholder':'Title of the site'}),
            'favicon ':forms.FileInput(attrs={'accept':"image/*", 'class':'form-control mt-2', 'placeholder':'Title of the site'}),
            'email':forms.EmailInput(attrs={'class':'form-control mt-2', 'placeholder':'Company Email..'}),
            'number_one':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Number of the site'}),
            'number_two':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Number 2 of the site'}),
            'address':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Address of the site'}),
        }



# Social Link
class SocialForm(forms.ModelForm):
   
   
    class Meta:
        model = SocialLink

        fields = ('__all__')

        widgets= {
            'name':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Facebook or Instagram or Gmail....'}),
            'icon':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'fa fa-facebook'}),
            'link':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'https://yoursite.com'}),
        }


# About Us form
class AboutForm(forms.ModelForm):
    class Meta:
        model = AboutUs
        fields = ('__all__')

        widgets= {
           
            'about_us':CKEditorUploadingWidget(attrs={'class':'form-control mt-2', 'placeholder':'About of the company'}),
            
        }


# Choose Us form
class ChooseForm(forms.ModelForm):
    class Meta:
        model = ChooseUs
        fields = ('__all__')

        widgets= {
           
            'choose':CKEditorUploadingWidget(attrs={'class':'form-control mt-2', 'placeholder':'About of the company'}),
            
        }

# Choose Us form
class HomeServiceForm(forms.ModelForm):
    class Meta:
        model = HomeService
        fields = ('__all__')

        widgets= {
            'service':CKEditorUploadingWidget(attrs={'class':'form-control mt-2', 'placeholder':'Home service description of the company'}),
        }

# Social Link
class FeatureForm(forms.ModelForm):
   
   
    class Meta:
        model = Feature

        fields = ('__all__')

        widgets= {
            'image':forms.FileInput(attrs={'accept':"image/*", 'class':'form-control mt-2'}),
            'name':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Features or Name....'}),
            'feature':CKEditorUploadingWidget(attrs={'class':'form-control mt-2', 'placeholder':'Features of the company'}),
            
        }


# About Us Form
class AboutForm(forms.ModelForm):

    class Meta:
        model = AboutUs

        fields = ('__all__')

        widgets= {
            'about_us':CKEditorUploadingWidget(attrs={'class':'form-control mt-2', 'placeholder':'About the company'}),
            'hide':forms.Select(attrs={'class':'form-control mt-2', 'placeholder':'Hide this navbar link?'}),
          
        }

class TermForm(forms.ModelForm):
    class Meta:
        model = Terms

        fields = ('__all__')

        widgets= {
            'terms':CKEditorUploadingWidget(attrs={'class':'form-control mt-2', 'placeholder':'Terms and condition of  the company'}),
        }


class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy

        fields = ('__all__')

        widgets= {
            'policy':CKEditorUploadingWidget(attrs={'class':'form-control mt-2', 'placeholder':'Policy of  the company'}),
        
        }


# Brand Form
class FootorForm(forms.ModelForm):
    class Meta:
        model = Footor

        fields = ('__all__')

        widgets= {
            'name':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Footor Title'}),
            'link':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'https://yoursite.com'}),
            'row':forms.Select(attrs={'class':'form-control mt-2'}),
        }

    # def selfForm(self, request):
    #     return FootorForm(request.POST, instance= self)

# Brand Form
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand

        fields = ('__all__')

        widgets= {
            'name':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Brand Name'}),
            'link':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'https://yoursite.com'}),
            'image':forms.FileInput(attrs={'accept':"image/*", 'class':'form-control mt-2', 'placeholder':'Image of Brand'}),
        }


class LoginInterfaceForm(forms.ModelForm):
     class Meta:
        model = LoginInterface
        fields = ('__all__')

        widgets= {
            'name':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Head of Login Page'}),
            'information':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Description Information of Login Page'}),
            'image':forms.FileInput(attrs={'accept':"image/*", 'class':'form-control mt-2', 'placeholder':'Description Information'}),
          
        }

class signupInterfaceForm(forms.ModelForm):
     class Meta:
        model = signupInterface
        fields = ('__all__')

        widgets= {
            'name':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Head of Login Page'}),
            'information':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Description Information'}),
            'image':forms.FileInput(attrs={'accept':"image/*", 'class':'form-control mt-2', 'placeholder':'Description Information'}),
            'video':forms.FileInput(attrs={'accept':"image/*", 'class':'form-control mt-2'}),
          
        }


class SEOForm(forms.ModelForm):
    class Meta:
        model = SEO
        fields = ('__all__')

        widgets= {
            'title':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Title of the page'}),
            'meta_description':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'This is a description of my web page.'}),
            'meta_keywords':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'keyword1, keyword2, keyword3'}),
            'canonical':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'https://www.example.com/my-page'}),
            'robot':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'index,follow'}),
            'og_title':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'My Web Page Title'}),
            'og_description':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'This is a description of my web page.'}),
            'og_image':forms.FileInput(attrs={'accept':"image/*", 'class':'form-control mt-2'}),
          
        }