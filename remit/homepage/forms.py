
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from homepage.models import Product, Service,Client, Testomonial, Blog, SubCategory, Category, Customer, Agent, Transaction
from homepage.models import CompanyInformation
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import password_validation




# Transaction Form
class TransactionForm(forms.ModelForm):


    class Meta:
        model = Transaction
        fields = ('__all__')
        



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
            visible.field.widget.attrs['class'] = 'form-control ps-0 form-control-line'

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
            'number': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Number'}),
            'mail_address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Mail Address'}),
            'state': forms.TextInput(attrs={'class':'form-control', 'placeholder':'You State'}),
            'zip_code' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Zip Code'}),
            'city' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}),
            'country' : forms.Select(attrs={'class':'form-control', 'placeholder':'Country'}),
            'address' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}),
            'profil_pic' : forms.FileInput(attrs={'class':'form-control', 'placeholder':'Profile Picture'}),
        }


class AgentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AgentForm, self).__init__(*args, **kwargs)
    
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control ps-0 form-control-line'

    class Meta:
      
        model = Agent

        fields = ('__all__')



class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        
        for fieldname in ['email',]:
            self.fields[fieldname].help_text = None
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control ps-0 form-control-line'
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
            visible.field.widget.attrs['class'] = 'form-control ps-0 form-control-line'

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
            visible.field.widget.attrs['class'] = 'form-control ps-0 form-control-line'

    class Meta:
        model = Service
        fields = ('name', 
                'description',
                'image',

                )
        labels = {
            'name':'Name of the Service',
            'description':'Description of Service',
            'image':'Image for Service',
    
        }
        widgets = {
            'description':CKEditorUploadingWidget
        }
   

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Create and Update Client Model ------------------->
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class ClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control ps-0 form-control-line'

    class Meta:
        model = Client
        fields = ('name', 
                'description',
                'image',
                'link'
     
                )
        labels = {
            'name':'Name of the Client',
            'description':'Description of Client',
            'image':'Image for Client',
            'link':'Link'
        }
        widgets = {
            'description':CKEditorUploadingWidget
        }
   
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Create and Update Testomonial Model ----------------->
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class TestomonialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TestomonialForm, self).__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control ps-0 form-control-line'

    class Meta:
        model = Testomonial
        fields = ('name', 
                'description',
           
                )
        labels = {
            'name':'Name of the Product',
            'description':'Description of Product',
         
        }
   

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Create and Update CompanyInformation Model -------------------->
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class CompanyInformationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CompanyInformationForm, self).__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control ps-0 form-control-line'

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
            'logo':forms.FileInput(attrs={'required':False})
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title','category','sub_category','description')

        labels = {
            'title':'Title of Blog*',
            'category':'Select Category*',
            'sub_category':'Select Sub Category',
            'description':'Description'
        }
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Add Your Title'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'sub_category':forms.Select(attrs={'class':'form-control mb-2'}),
            'description':CKEditorUploadingWidget
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
            self.fields['old_password'].widget.attrs = {'class':'form-control ps-0 form-control-line', 'placeholder':"Old Password"}
            self.fields['new_password1'].widget.attrs = {'class':'form-control ps-0 form-control-line', 'placeholder':"New Password"}
            self.fields['new_password2'].widget.attrs = {'class':'form-control ps-0 form-control-line', 'placeholder':"Re New Password"}