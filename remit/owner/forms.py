from django import forms
from homepage.models import Feature, AboutUs, ChooseUs, HomeService, Brand ,LoginInterface, signupInterface, Policy, Footor, Service, Client, Testomonial, Terms, SocialLink, TopHeader, CompanyInformation
from .models import SiteSetting, SEO
from ckeditor_uploader.widgets import CKEditorUploadingWidget



class SiteForm(forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = ('__all__')

        widgets= {
            'title':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Title of the site'}),
            'subtitle':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Sub title of the site'}),
            'light_logo':forms.FileInput(attrs={'class':'form-control mt-2', 'placeholder':'Title of the site'}),
            'dark_logo ':forms.FileInput(attrs={'class':'form-control mt-2', 'placeholder':'Title of the site'}),
            'favicon ':forms.FileInput(attrs={'class':'form-control mt-2', 'placeholder':'Title of the site'}),
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
            'image':forms.FileInput(attrs={'class':'form-control mt-2', 'placeholder':'Image of Brand'}),
        }


class LoginInterfaceForm(forms.ModelForm):
     class Meta:
        model = LoginInterface
        fields = ('__all__')

        widgets= {
            'name':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Head of Login Page'}),
            'information':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Description Information of Login Page'}),
            'image':forms.FileInput(attrs={'class':'form-control mt-2', 'placeholder':'Description Information'}),
          
        }

class signupInterfaceForm(forms.ModelForm):
     class Meta:
        model = signupInterface
        fields = ('__all__')

        widgets= {
            'name':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Head of Login Page'}),
            'information':forms.TextInput(attrs={'class':'form-control mt-2', 'placeholder':'Description Information'}),
            'image':forms.FileInput(attrs={'class':'form-control mt-2', 'placeholder':'Description Information'}),
            'video':forms.FileInput(attrs={'class':'form-control mt-2'}),
          
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
            'og_image':forms.FileInput(attrs={'class':'form-control mt-2'}),
          
        }