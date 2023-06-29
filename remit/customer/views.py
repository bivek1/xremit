from django.shortcuts import render
from owner.forms import RecipientForm, Recipient, KYC, KYCForm
from homepage.models import Currency
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View
from homepage.forms import PasswordChangeFormUpdate, CustomerForm, Customer





# Create your views here.
def customerDashboard(request):
    dist = {
        'currency' : Currency.objects.all().order_by('-id')[:3]
    }
    return render(request, "customer/dashboard.html", dist)

def recipient(request):
    
    recipient = Recipient.objects.all().order_by('-id')
    dist = {
        'recipient':recipient
    }

    return render(request, "customer/recipient.html", dist)



def addRecipient(request):
    form = RecipientForm()
    recipient = Recipient.objects.all().order_by('-id')
    dist = {
        'recipient':recipient,
        'form':form
    }

    if request.method == 'POST':
        form = RecipientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added recipient")
            return HttpResponseRedirect(reverse('customer:recipient'))
        else:
            messages.error(request,"Something went wrong")
            

    return render(request, "customer/addRecipient.html", dist)

def editRecipient(request, id):
    
    rec = Recipient.objects.get(id = id)
    form = RecipientForm(instance=rec)
    recipient = Recipient.objects.all().order_by('-id')
    dist = {
        'recipient':recipient,
        'form':form
    }

    if request.method == 'POST':
        form = RecipientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated recipient")
            return HttpResponseRedirect(reverse('customer:recipient'))
        else:
            messages.error(request,"Something went wrong")
            

    return render(request, "customer/editRecipient.html", dist)


def deleteRecipient(request, id):
    rec = Recipient.objects.get(id = id)
    rec.delete()
    messages.success(request, "Successfully Deleted Recipient")
    return HttpResponseRedirect(reverse('customer:recipient'))

def sendMoney(request):
    return render(request, "customer/sendMoney.html")

def currency(request):
    currency = Currency.objects.all().order_by('-id')

    dist ={
        'currency':currency
    }
    return render(request, "customer/currency.html", dist)

def kycVerify(request):

    form = KYCForm

    dist = {
        'form':form
    }

    if request.method == 'POST':
        form = KYCForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully sent for verification")
    return render(request, "customer/verify.html", dist)


class Profile(View):
    template_name = 'customer/profile.html'
    def get(self, request, *args, **kwargs):
        pcform = PasswordChangeFormUpdate(request.user)
        form = CustomerForm(instance=request.user.customer)
        
        dist = {
            'pcform':pcform,
            'form':form,
            'real_customer':request.user.customer
              
        }
        return render(request, self.template_name, dist)

    def post(self, request, *args, **kwargs):
        real_customer = request.user.customer
        if request.method == 'POST':
            try: 
                real_customer.admin.first_name = request.POST['first_name']
                real_customer.admin.last_name = request.POST['last_name']
                real_customer.admin.email = request.POST['email']
                real_customer.admin.username = request.POST['email']
                real_customer.admin.save()
            except:
                messages.error(request, "Email is added already..")
                return HttpResponseRedirect(reverse('customer:profile'))
            form = CustomerForm(request.POST, instance=real_customer)
            if form.is_valid():
                form.save()
                messages.success(request, "Successfully Updated Customer")
                return HttpResponseRedirect(reverse('customer:profile'))
            else:
                messages.error(request, "Something went wrong")

            messages.success(request, "Sucessfully Updated Profile")
        return HttpResponseRedirect(reverse('customer:profile'))