from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from .models import Feature, Service, Client, Testomonial, Footor, Brand, AboutUs, ChooseUs, HomeService
from .models import Blog
from django.contrib.auth import authenticate
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout
# Create your views here.
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

    service = Service.objects.all().order_by('-id')[:5]
    testomonial = Testomonial.objects.all().order_by('-id')[:5]
    client = Client.objects.all().order_by('-id')[:5]
    feature = Feature.objects.all().order_by('-id')[:5]
    brand = Brand.objects.all().order_by('-id')[:5]
    
    dist = {
        'choose':choose,
        'about':about,
        'homes':homes,
        'service':service,
        'testomonial':testomonial,
        'client':client,
        'feature':feature,
        'brand':brand
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
            return HttpResponseRedirect(reverse('owner:dashboard'))
        else:
            messages.error(request, "Incorrect Username and Password")
            return render(request, tempate_name)
    else:
        return render(request, tempate_name)
    

def Register(request):

    tempate_name = 'homepage/register.html'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        use = authenticate(request, username = username, password = password)
        if use is not None:
            login(request, use)
            return HttpResponseRedirect(reverse('manager:dashboard'))
        else:
            messages.error(request, "Incorrect Username and Password")
            return render(request, tempate_name)
    else:
        return render(request, tempate_name)
    
def LogoutV(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage:login'))