from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView
from .models import LoginInterface, signupInterface, Feature, Service, Client, Testomonial, Footor, Brand, AboutUs, ChooseUs, HomeService
from .models import Blog, CustomUser
from django.contrib.auth import authenticate
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout
from .forms import PasswordChangeFormUpdate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .forms import ContactForm
from homepage.models import Currency,SocialLink, Country, DefaultCurrencyAdmin, LoginLogs, OTPcode, DefaultCurrencyAdmin
# Create your views here.
from .location import get_user_country
from owner.models import BlockPlace
from .ipaddress import log_user_login
from django.http import JsonResponse
from owner.models import SiteSetting
from .otp import generate_random_code
from django.conf import settings

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags



def changeCurone(request):
    if request.method == 'POST':
        my_data = request.POST.get('id')  # Get the sent data
        currency = Currency.objects.get(id = int(my_data))
        print(currency)
        # Process the data and prepare the response
        response_data = {
            'currency_rate':  currency.currecy_rate,
            'fee' : currency.conversion_rate,
            'cur_sign' : currency.currecy_sign
        }

        return JsonResponse(response_data)  # Return the response as JSON



def set_session_small(request):
    request.session['navbar'] = 'small'
    return JsonResponse({'status':'ok'})

def set_session_big(request):
    request.session['navbar'] = 'big'
    return JsonResponse({'status':'ok'})


def siteInfo():
    site = SiteSetting.objects.all()    
    if site:
        for i in site:
            site = i
            break
    dist ={
        'site':site
    }
    return dist

# Password Reset form
def checkPassword(request):
   if request.method == 'POST':
        form = PasswordChangeFormUpdate(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            
        else:
            error = form.errors.as_data()
            messages.error(request, error)
        if request.user.user_type == 'owner':
            return HttpResponseRedirect(reverse('superuser:profile'))
        elif request.user.user_type == 'agent':
            return HttpResponseRedirect(reverse('agent:profile'))
        else:
            return HttpResponseRedirect(reverse('customer:profile'))
   
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = CustomUser.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

def handler404(request, exception):
    return render(request, 'homepage/404.html', status=404)



def Homepage(request):
    template_name = 'homepage/index.html'
    choose = ChooseUs.objects.all()
   

    if choose:
        for i in choose:
            choose = i
            break

    # About Us
    about = AboutUs.objects.all()
    
    if about:
        for i in about:
            about = i
            break

    # Home Service
    homes = HomeService.objects.all()
    
    if homes:
        for i in homes:
            homes = i
            break

  
    testomonial = Testomonial.objects.all()[:5]
    client = Client.objects.all().order_by('-id')[:5]

    brand = Brand.objects.all().order_by('-id')[:4]
    asa = DefaultCurrencyAdmin.objects.all()
    if asa:
        for i in asa:
            asa = i
            break
    try:
        default = asa.sending_currency
    except:
        default = Currency.objects.last()   

    try:
        re_default = asa.receiving_currency
    except:
        re_default = Currency.objects.first()     
   
    dist = {
        'choose':choose,
        'about':about,
        'homes':homes,
        'service_man':Service.objects.all()[:4],
        'testomonial':testomonial,
        'social':SocialLink.objects.all(),
        'client':client,
        'feature_b':Feature.objects.all()[:4],
        'brand':brand,
        'currency':Currency.objects.all()[:4],
        'country': Country.objects.all(),
        'blog':Blog.objects.all()[:6],
        'default':default,
        're_default':re_default,
        'first_fo':Footor.objects.filter(row='First'),
        'second_fo':Footor.objects.filter(row='Second'),
        'third_fo':Footor.objects.filter(row='Third'),
    }
    other_info = siteInfo()
    dist.update(other_info)

    return render(request, template_name, dist)
    

class BlogV(DetailView):
    model = Blog
    template_name = "homepage/blog.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


import random
def OPTV(request):
    
   
    if request.method == 'POST':

        get_code = request.POST['otp']
        print(code)
        print(request.user.customer.customer_otp.code , get_code)
        if get_code == request.user.customer.customer_otp.code:
            return HttpResponseRedirect(reverse('customer:dashboard'))
        else:
            messages.error(request, "Invalid OPT. Try again")
    else:
        code = int(random.randint(1000, 9999))
        print(code)
        try:
            op = request.user.customer.customer_otp
            op.code = code
            op.save()
        except:
            op = OTPcode.objects.create(customer = request.user.customer, code = code)
            op.save()
        
        
    return render(request, "homepage/otp.html")

def LoginV(request):
    social=SocialLink.objects.all()
    loginss = LoginInterface.objects.all()
    for i in loginss:
        loginss = i
        break
    dist = {
        'social':social,
        'first_fo':Footor.objects.filter(row='First'),
        'second_fo':Footor.objects.filter(row='Second'),
        'third_fo':Footor.objects.filter(row='Third'),
        'info':loginss

    }

    dist.update(siteInfo())
    tempate_name = 'homepage/login.html'
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        use = authenticate(request, username = username, password = password)
        if use is not None:
            login(request, use)
            if use.user_type == 'owner':
                return HttpResponseRedirect(reverse('owner:dashboard'))
            elif use.user_type == "customer":
                if use.customer.security == 'sms':
                    # return HttpResponseRedirect(reverse('homepage:OTPV'))
                    return HttpResponseRedirect(reverse('customer:dashboard'))
                else:
                    return HttpResponseRedirect(reverse('customer:dashboard'))
            else:
                return HttpResponseRedirect(reverse('agent:dashboard'))
        else:
            messages.error(request, "Incorrect Username and Password")
            return render(request, tempate_name)
    else:
        # blok = get_user_country()
    
        # blockPlac = BlockPlace.objects.filter(block_status = True)
        # for i in blockPlac:
        #     if i.block == "Country":
        #         if blok['country'] == i.name or blok['region'] == i.name or blok['city'] == i.name :
        #             return render(request, 'homepage/blocked.html')
        if request.user.is_authenticated:
            if request.user.user_type == 'owner':
                return HttpResponseRedirect(reverse('owner:dashboard'))
            elif request.user.user_type == "customer":
                return HttpResponseRedirect(reverse('customer:dashboard'))
            else:
                return HttpResponseRedirect(reverse('agent:dashboard'))
        else:
            return render(request, tempate_name, dist)
    

def Register(request):
    sisas = signupInterface.objects.all()
    for i in sisas:
        sisas = i 
        break
    dist = {
        'social':SocialLink.objects.all(),
        'first_fo':Footor.objects.filter(row='First'),
        'second_fo':Footor.objects.filter(row='Second'),
        'third_fo':Footor.objects.filter(row='Third'),
        'sisas':sisas

    }
    dist.update(siteInfo())
    tempate_name = 'homepage/register.html'
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['email']
        password = request.POST['password']
        recipient_list = []
        try:
            admin = CustomUser.objects.create_user(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], username = request.POST['email'], password = request.POST['password'], user_type = 'customer')
            obj = admin.customer
            obj.added_by = admin
            obj.save()
            recipient_list.append(admin.email)
           
        except:
            messages.error(request, "Email is already registered please try again with different email")
            return HttpResponseRedirect(reverse('homepage:register'))
        use = authenticate(request, username = username, password = password)
        if use is not None:
            login(request, use)
            content = settings.EMAIL_HOST_USER
            sub = 'Successfully Created Account Syon Remit'
            messa = "Syon Remit Welcome you to the easy money transfering app. Thank you for the registration."
            other_info = siteInfo()
    
            dist_info = {
                'sub': sub, 'message':messa,
              
            }
            dist_info.update(other_info)
            html_message = render_to_string('component/email.html', dist_info)
            pain_html_msg = strip_tags(html_message)
            # try: 
            msg = EmailMultiAlternatives(sub, pain_html_msg, content, recipient_list)
            msg.attach_alternative(html_message, "text/html")
            msg.send()
            # except:pass
            messages.success(request, "Successfully Registered")
            return HttpResponseRedirect(reverse('customer:dashboard'))
        else:
            messages.error(request, "Incorrect Username and Password")
            return render(request, tempate_name, dist)
    else:
        blok = get_user_country()
    
        blockPlac = BlockPlace.objects.filter(block_status = True)
        for i in blockPlac:
            if i.block == "Country":
                if blok['country'] == i.name or blok['region'] == i.name or blok['city'] == i.name :
                    return render(request, 'homepage/blocked.html')
        return render(request, tempate_name, dist)
    
def LogoutV(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage:login'))


def serviceView(request):
    dist = {
        'service_man':Service.objects.all(),
        'social':SocialLink.objects.all(),
        'first_fo':Footor.objects.filter(row='First'),
        'second_fo':Footor.objects.filter(row='Second'),
        'third_fo':Footor.objects.filter(row='Third'),
    }
    dist.update(siteInfo())
    return render(request, "homepage/other/service.html", dist)

def serviceDetail(request, id, name):
    service = Service.objects.get(id = id)
    dist = {
        'service_man':Service.objects.all(),
        'service':service,
        'social':SocialLink.objects.all(),
        'first_fo':Footor.objects.filter(row='First'),
        'second_fo':Footor.objects.filter(row='Second'),
        'third_fo':Footor.objects.filter(row='Third'),
    }
    dist.update(siteInfo())
    return render(request, "homepage/other/serviceDetail.html", dist)


def aboutView(request):
    # About Us
    about = AboutUs.objects.all()
    
    if about:
        for i in about:
            about = i
            break

    dist = {
        'service_man':Service.objects.all(),
        'social':SocialLink.objects.all(),
        'about':about,
        'feature_b':Feature.objects.all(),
        'first_fo':Footor.objects.filter(row='First'),
        'second_fo':Footor.objects.filter(row='Second'),
        'third_fo':Footor.objects.filter(row='Third'),
    }
    dist.update(siteInfo())
    return render(request, "homepage/other/about.html", dist)

def blogView(request):
    dist = {
        'service_man':Service.objects.all(),
        'social':SocialLink.objects.all(),
        'blog':Blog.objects.all().order_by('-id'),
        'first_fo':Footor.objects.filter(row='First'),
        'second_fo':Footor.objects.filter(row='Second'),
        'third_fo':Footor.objects.filter(row='Third'),
    }
    dist.update(siteInfo())
    return render(request, "homepage/other/blog.html", dist)

def blogDetail(request, id, name):
    blog = Blog.objects.get(id = id)
    dist = {
        'blog_man':Blog.objects.all(),
        'blog':blog,
        'social':SocialLink.objects.all(),
        'first_fo':Footor.objects.filter(row='First'),
        'second_fo':Footor.objects.filter(row='Second'),
        'third_fo':Footor.objects.filter(row='Third'),
    }
    dist.update(siteInfo())
    return render(request, "homepage/other/blogDetail.html", dist)

def countryView(request):
    dist = {
        'service_man':Service.objects.all(),
        'social':SocialLink.objects.all(),
        'country':Country.objects.all().order_by('-id'),
        'first_fo':Footor.objects.filter(row='First'),
        'second_fo':Footor.objects.filter(row='Second'),
        'third_fo':Footor.objects.filter(row='Third'),
    }
    dist.update(siteInfo())
    return render(request, "homepage/other/country.html", dist)

def currencyView(request):
    dist = {
        'service_man':Service.objects.all(),
        'social':SocialLink.objects.all(),
        'default' : Currency.objects.last(),
        'currency':Currency.objects.all().order_by('-id'),
        'first_fo':Footor.objects.filter(row='First'),
        'second_fo':Footor.objects.filter(row='Second'),
        'third_fo':Footor.objects.filter(row='Third'),
    }
    dist.update(siteInfo())
    return render(request, "homepage/other/currency.html", dist)

def featureView(request):
    dist = {
        'service_man':Service.objects.all(),
        'feature_b':Feature.objects.all(),
        'social':SocialLink.objects.all(),
        'first_fo':Footor.objects.filter(row='First'),
        'second_fo':Footor.objects.filter(row='Second'),
        'third_fo':Footor.objects.filter(row='Third'),
    }
    dist.update(siteInfo())
    return render(request, "homepage/other/feature.html", dist)

def featureDetail(request, id, name):
    feature = Feature.objects.get(id = id)
    dist = {
        'feature_man':Feature.objects.all(),
        'feature':feature,
        'social':SocialLink.objects.all(),
        'first_fo':Footor.objects.filter(row='First'),
        'second_fo':Footor.objects.filter(row='Second'),
        'third_fo':Footor.objects.filter(row='Third'),
    }
    dist.update(siteInfo())
    return render(request, "homepage/other/featureDetail.html", dist)

def sitemapView(request):
    dist = {
        'service_man':Service.objects.all(),
        'social':SocialLink.objects.all(),
        'first_fo':Footor.objects.filter(row='First'),
        'second_fo':Footor.objects.filter(row='Second'),
        'third_fo':Footor.objects.filter(row='Third'),
    }
    dist.update(siteInfo())
    return render(request, "homepage/other/sitemap.html", dist)

def privacyView(request):
    dist = {
        'service_man':Service.objects.all(),
        'social':SocialLink.objects.all(),
        'first_fo':Footor.objects.filter(row='First'),
        'second_fo':Footor.objects.filter(row='Second'),
        'third_fo':Footor.objects.filter(row='Third'),
    }
    dist.update(siteInfo())
    return render(request, "homepage/other/privacy.html", dist)

def termsView(request):
    dist = {
        'service_man':Service.objects.all(),
        'social':SocialLink.objects.all(),
        'first_fo':Footor.objects.filter(row='First'),
        'second_fo':Footor.objects.filter(row='Second'),
        'third_fo':Footor.objects.filter(row='Third'),
    }
    dist.update(siteInfo())
    return render(request, "homepage/other/terms.html", dist)

def contactView(request):
    form = ContactForm()
    dist = {
        'form':form,
        'social':SocialLink.objects.all(),
        'first_fo':Footor.objects.filter(row='First'),
        'second_fo':Footor.objects.filter(row='Second'),
        'third_fo':Footor.objects.filter(row='Third'),
    }
    
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Successfully sent messages")
    return render(request, "homepage/other/contact.html", dist)