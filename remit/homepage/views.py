from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView
from .models import Feature, Service, Client, Testomonial, Footor, Brand, AboutUs, ChooseUs, HomeService
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
from django.core.mail import send_mail
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from homepage.models import Currency,SocialLink
# Create your views here.



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





def Homepage(request):
    template_name = 'homepage/index.html'
    choose = ChooseUs.objects.all()
    try:
        default = request.user.customer.customer_currency.currency
    except:
        default = Currency.objects.last()

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

    service = Service.objects.all().order_by('-id')[:5],
    test_last = Testomonial.objects.last()
    testomonial = Testomonial.objects.all().exclude(id = test_last.id)[:5]
    client = Client.objects.all().order_by('-id')[:5]
    feature = Feature.objects.all().order_by('-id')[:5]
    brand = Brand.objects.all().order_by('-id')[:4]
    
    dist = {
        'choose':choose,
        'about':about,
        'homes':homes,
        'service':service,
        'last_test':test_last,
        'testomonial':testomonial,
        'social':SocialLink.objects.all(),
        'client':client,
        'feature':feature,
        'brand':brand,
        'currency':Currency.objects.all(),
        'default':default,
        'first_fo':Footor.objects.filter(row='First'),
        'second_fo':Footor.objects.filter(row='Second'),
        'third_fo':Footor.objects.filter(row='Third'),
    }

    return render(request, template_name, dist)
    


class BlogV(DetailView):
    model = Blog
    template_name = "homepage/blog.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


def LoginV(request):

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
                return HttpResponseRedirect(reverse('customer:dashboard'))
        else:
            messages.error(request, "Incorrect Username and Password")
            return render(request, tempate_name)
    else:
        return render(request, tempate_name)
    

def Register(request):
    dist = {
        'social':SocialLink.objects.all()
    }
    tempate_name = 'homepage/register.html'
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['email']
        password = request.POST['password']
        try:
            admin = CustomUser.objects.create_user(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], username = request.POST['email'], password = request.POST['password'], user_type = 'customer')
            obj = admin.customer
            obj.added_by = admin
            obj.save()
        except:
            messages.error(request, "Email is already registered please try again with different email")
            return HttpResponseRedirect(reverse('homepage:register'))
        use = authenticate(request, username = username, password = password)
        if use is not None:
            login(request, use)
            messages.success(request, "Successfully Registered")
            return HttpResponseRedirect(reverse('customer:dashboard'))
        else:
            messages.error(request, "Incorrect Username and Password")
            return render(request, tempate_name, dist)
    else:
        return render(request, tempate_name, dist)
    
def LogoutV(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage:login'))