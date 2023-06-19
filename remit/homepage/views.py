from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from .models import Blog
from django.contrib.auth import authenticate
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout
# Create your views here.
class Homepage(TemplateView):
    template_name = 'homepage/index.html'



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