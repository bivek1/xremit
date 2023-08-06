
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from homepage.models import AdminBankAccount, Product, Service,Client, Testomonial, Blog, SubCategory, Category, Customer, Agent, Transaction
from homepage.models import CompanyInformation, BankAccount, Contact, Ticket, TicketReply, Restriction
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import password_validation



# Admin Bank Account Form
class AdminBankForm(forms.ModelForm):
    
    class Meta:
        model = AdminBankAccount
        fields = ('__all__')

        widgets= {
            'account_name': forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Adam Smith'}),
            'account_number': forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'02264871564112121BA'}),
            'bank_name': forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Australian High Com Bank'}),
            'country': forms.Select(attrs={'class':'form-control mt-2','placeholder':'Australia'}),
            'swift_code': forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'AHCB21S'}),
            'branch': forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Melbourne, VIC'}),
        }

# Support Ticket


class RestrictionForm(forms.ModelForm):
    class Meta:
        model = Restriction
        fields = ('__all__')
    
        widgets= {
            'minimum_amount': forms.NumberInput(attrs={'class':'form-control mt-2', 'placeholder':'Minumum Transfer Limit'}),
            'maximum_amount': forms.NumberInput(attrs={'class':'form-control mt-2', 'placeholder':'Maximum Transfer Limit'}),
            'daily_transfer_remit': forms.NumberInput(attrs={'class':'form-control mt-2', 'placeholder':'Daily Transfer Limit'}),
            'maximum_cap_charge': forms.NumberInput(attrs={'class':'form-control mt-2', 'placeholder':'Maximum Cap Charge'}),
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('__all__')
        exclude = ('customer',)

        widgets= {
        
            'subject': forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Subject of your ticket'}),
            'piority': forms.Select(attrs={'class':'form-control mt-2', 'placeholder':'Australian High Com Bank'}),
            'department': forms.Select(attrs={'class':'form-control mt-2','placeholder':'Australia'}),
            'description': CKEditorUploadingWidget()
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = TicketReply
        fields = ('__all__')
        exclude = ('replied_by',)

        widgets= {
    
            'description': forms.Textarea(attrs={'class':'form-control reply-ticket', 'placeholder':'Write your reply here...'}),
            'ticket':forms.Select(attrs={'hidden':True})
        }

# Transaction Form
class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
      
        # for visible in self.visible_fields():
        #     visible.field.widget.attrs['hidden'] = True
    class Meta:
        model = Transaction
        fields = ('__all__')
    
# Transaction Form
class BankForm(forms.ModelForm):
    
    class Meta:
        model = BankAccount
        fields = ('__all__')
        exclude = ('customer','recipient',)

        widgets= {
            'account_name': forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Adam Smith'}),
            'account_number': forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'02264871564112121BA'}),
            'bank_name': forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Australian High Com Bank'}),
            'country': forms.Select(attrs={'class':'form-control mt-2','placeholder':'Australia'}),
            'branch': forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Melbourne, VIC'}),
            'swift_code': forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'AHCB21S'}),
        }



class PasswordChangeFormUpdate(PasswordChangeForm):
    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-control', 'placeholder':'Enter New Password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-control', 'placeholder':'Enter New Password Again'}),
    )
    old_password = forms.CharField(
        label=("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True , 'class':'form-control', 'placeholder':'Enter Your Old Password'}
        ),
    )

# User Create and Update form
class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        
        for fieldname in ['email', 'password']:
            self.fields[fieldname].help_text = None
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control  form-control-line'

    class Meta:
        model = User
        fields = ('first_name', 
                'last_name',
                'username',
                'email',
                'password',)
        labels = {
                'first_name':'First Name',
                'last_name':'Last Name',
                'username':'Username',
                'email':'Email',
                'password':'Password'
        }
   

class CustomerForm(forms.ModelForm):
   
    class Meta:
      
        model = Customer

        fields = ('__all__')

        widgets = {
            'number': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'+61 4 91 575 789'}),
            'mail_address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'14428. Melbourne, VIC 8001'}),
            'state': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Victoria'}),
            # 'zip_code' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'30001'}),
            'city' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Melbourne'}),
            'country' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Australia'}),
            'address' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'123 Smith Street, Richmond, Victoria'}),
            'profil_pic' : forms.FileInput(attrs={'accept':"image/*", 'class':'form-control', 'placeholder':'Profile Picture'}),
        }


class AgentForm(forms.ModelForm):

    class Meta:
      
        model = Agent

        fields = ('__all__')
        
        widgets = {
            'number': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'+61 4 91 575 789'}),
            'mail_address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'14428. Melbourne, VIC 8001'}),
            'state': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Victoria'}),
            'zip_code' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'30001'}),
            'city' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Melbourne'}),
            'country' : forms.Select(attrs={'class':'form-control', 'placeholder':'Australia'}),
            'address' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'123 Smith Street, Richmond, Victoria'}),
            'profil_pic' : forms.FileInput(attrs={'accept':"image/*", 'class':'form-control', 'placeholder':'Profile Picture'}),
        }



class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        
        for fieldname in ['email',]:
            self.fields[fieldname].help_text = None
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control  form-control-line'
    class Meta:
      
        model = User

        fields = ('first_name', 
                'last_name',
                'username',
                'email',)
        labels = {
            'first_name':'First Name',
            'last_name':'Last Name',
            'username':'Username',
            'email':'Email',
        }

# Create and Update Product
class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control  form-control-line'

    class Meta:
        model = Product
        fields = ('name', 
                'description',
                'image',
                'link',
                )
        labels = {
            'name':'Name of the Product',
            'description':'Description of Product',
            'image':'Image for Product',
            'link':'Link',
        }
   

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Create and Update Service Model ------------------->
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class ServiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control  form-control-line'

    class Meta:
        model = Service
        fields = ('name', 
                'description',
                'image',

                )
        labels = {
            'name':'Name of the Service*',
            'description':'Description of Service*',
            'image':'Image for Service*',
    
        }
        widgets = {
            'description':CKEditorUploadingWidget(),
            'name':forms.TextInput(attrs={'placeholder':'Name of the your service...'}),
            
        }   
   

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Create and Update Client Model ------------------->
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class ClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control  form-control-line'

    class Meta:
        model = Client
        fields = ('name', 
                'description',
                'image',
                'link'
     
                )
        labels = {
            'name':'Name of the Client*',
            'description':'Description of Client',
            'image':'Image of Client/Company',
            'link':'Link'
        }
        widgets = {
            'description':CKEditorUploadingWidget(),
            'name':forms.TextInput(attrs={'placeholder':'Name of the your client...'}),
            'link':forms.TextInput(attrs={'placeholder':'Url link of the client if avaiable...'}),
        }
   
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Create and Update Testomonial Model ----------------->
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class TestomonialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TestomonialForm, self).__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control  form-control-line'

    class Meta:
        model = Testomonial
        fields = ('name', 
                'description',
           
                )
        labels = {
            'name':'Name of the User*',
            'description':'Description*',
        },
        widgets = {
            'name':forms.TextInput(attrs={'placeholder':'Name of the user '}),
            'description':forms.TextInput(attrs={'placeholder':'Write what they say about you..'})
        }
   

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Create and Update CompanyInformation Model -------------------->
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class CompanyInformationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CompanyInformationForm, self).__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control  form-control-line'

    class Meta:
        model = CompanyInformation
        fields = ('name', 
                'short',
                'aims',
                'logo',
                )
        labels = {
            'name':'Name',
            'short':'Short Description of Company',
            'logo':'Company Logo',
            'aims':'Aims',
        }
        widgets = {
            'logo':forms.FileInput(attrs={'accept':"image/*", 'required':False})
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'types', 'image','description')

        labels = {
            'title':'Title of Blog*',
            'description':'Description'
        }
        widgets = {
            'image':forms.FileInput(attrs={'accept':"image/*", 'class':'form-control mt-2'}),
            'title':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Add Your Title'}),
            'types':forms.Select(attrs={'class':'form-control mt-2'}),
            'description':CKEditorUploadingWidget()
        }


# Contact Form
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'number','message')

        labels = {
            'name':'Full name*',
            'email':'Your valid email address*',
            'number':'Your valid number*',
            'message':'Your your message here*',
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Your Full Name'}),
            'email':forms.EmailInput(attrs={'class':'form-control mt-2', 'placeholder':'robertthopson23@hotmail.com'}),
            'number':forms.NumberInput(attrs={'class':'form-control mt-2', 'placeholder':'+61 717 7118 171'}),
            'message':forms.Textarea(attrs={'class':'form-control mt-2' ,'placeholder':'Write your message here..'})
        }

# Category Form

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

        labels = {
            'name':'Name of Category*',
          
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Category Name'}),
        }

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ('name','category')

        labels = {
            'name':'Name of SubCategory*',
            'category':'Category'
            
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Category Name'}),
            'category':forms.Select(attrs={'class':'form-control mb-2'}),
        }


from django.contrib.auth.forms import PasswordChangeForm

class FormChangePassword(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(FormChangePassword, self).__init__(*args, **kwargs)
        for field in ('old_password', 'new_password1', 'new_password2'):
            self.fields['old_password'].widget.attrs = {'class':'form-control  form-control-line', 'placeholder':"Old Password"}
            self.fields['new_password1'].widget.attrs = {'class':'form-control  form-control-line', 'placeholder':"New Password"}
            self.fields['new_password2'].widget.attrs = {'class':'form-control  form-control-line', 'placeholder':"Re New Password"}