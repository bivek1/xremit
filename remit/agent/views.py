from django.shortcuts import render
from homepage.forms import AgentForm, PasswordChangeFormUpdate
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View
from homepage.models import Country, Currency
from owner.forms import CurrencyForm

# Create your views here.
def dashboard(request):
    dist = {
        'currency':Currency.objects.all()
    }
    return render(request, "agent/dashboard.html", dist)

class Profile(View):
    template_name = 'agent/profile.html'
    def get(self, request, *args, **kwargs):
        pcform = PasswordChangeFormUpdate(request.user)
        form = AgentForm(instance=request.user.agent)
        
        dist = {
            'pcform':pcform,
            'form':form,
        
            'real_customer':request.user.agent
              
        }

        return render(request, self.template_name, dist)

    def post(self, request, *args, **kwargs):
        real_customer = request.user.agent
        try:
            real_customer.admin.first_name = request.POST['first_name']
            real_customer.admin.last_name = request.POST['last_name']
            real_customer.admin.email = request.POST['email']
            real_customer.admin.username = request.POST['email']
            real_customer.admin.save()
        except:
            messages.error(request, "Email is added already..")
            return HttpResponseRedirect(reverse('agent:profile'))
        form = AgentForm(request.POST)
        if form.is_valid():
            real_customer.number = request.POST['number']
            real_customer.mail_address = request.POST['mail_address']
            real_customer.state = request.POST['state']
            real_customer.zip_code = request.POST['zip_code']
            real_customer.city = request.POST['city']
            real_customer.country= Country.objects.get(id = request.POST['country'])
            real_customer.address = request.POST['address']
            real_customer.save()
            
            messages.success(request, "Sucessfully Updated Profile")
            return HttpResponseRedirect(reverse('agent:profile'))
        else:
            err = form.errors
            print(err)
            messages.error(request, "Something went wrong")
            return render(request, self.template_name, self.get.dist)
        
def updatePic(request):
    file = request.FILES['profile']
    cust = request.user.agent
    cust.profil_pic = file
    cust.save()
    messages.success(request, "Successfully updated profile picture")
    return HttpResponseRedirect(reverse('agent:profile'))

def currencyView(request):
    currency = Currency.objects.all().order_by('-id')
    form = CurrencyForm()
    dist = {
        'currency':currency,
        'form': form,
        'country':Country.objects.all()
    }

    if request.method == 'POST':
        form = CurrencyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added new currency")
            return HttpResponseRedirect(reverse('agent:currency'))
        else:
            dist.update({'form':form})
            messages.error(request,"something went wrong")

    return render(request, "agent/currency.html", dist)


def editCurrency(request, id):
    currency = Currency.objects.get(id = id)
    currency.country = Country.objects.get(id =request.POST['country']) 
    currency.currecy_rate = request.POST['currecy_rate']
    currency.conversion_rate = request.POST['conversion_rate']
    currency.commision_rate = request.POST['commision_rate']
    currency.currecy_sign = request.POST['currecy_sign']
    currency.save()
    messages.success(request, "Successfully Edited Currency")
    return HttpResponseRedirect(reverse('agent:currency'))



def deleteCurrency(request, id):
    footer = Currency.objects.get(id = id)
    footer.delete()
    messages.success(request, "Successfully deleted currency")
    return HttpResponseRedirect(reverse('agent:currency'))