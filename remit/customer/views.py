from django.shortcuts import render
from owner.forms import RecipientForm, Recipient, KYC, KYCForm
from homepage.models import Currency, Country, Transaction, BankAccount, DefaultCurrency, SupportFile, Ticket
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View
from homepage.forms import PasswordChangeFormUpdate, CustomerForm, TicketForm
from django.http import JsonResponse
from homepage.forms import TransactionForm, BankForm, ReplyForm
from django.core import serializers
from homepage.models import CustomerNotification, Ticket, AdminNotification
    



def search(request):
    query = request.GET.get('search')
    reciepient = Recipient.objects.filter(first_name__icontains=query).filter(customer = request.user.customer)
    bank = BankAccount.objects.filter(account_name__icontains=query).filter(customer = request.user.customer)
    currency = Currency.objects.filter(country__name__icontains=query)
    dist = {
        'reciepient':reciepient,
        'bank':bank,
        'currency':currency,
        'noti': CustomerNotification.objects.filter(seen= False),
        'noti_count' : CustomerNotification.objects.filter(seen= False).count(),
    }
    return render(request, 'customer/search.html', dist)

def seenNotification(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print(id)  
        tic = CustomerNotification.objects.get(id = int(id))

        tic.seen = True
        tic.save()
        return JsonResponse({'staus':'ok'})

   

def notification():
   noti = CustomerNotification.objects.filter(seen= False)
   count = noti.count()

   li = {
       'noti':noti,
       'noti_count':count
   }
   return li


def allNotification(request):
    noti = CustomerNotification.objects.all().order_by('-id')
    count = noti.count()

    dist = {
        'noti':noti,
        'noti_count':count
    }
    noti = notification()
    dist.update(noti)
    return render(request, "customer/notification.html", dist)

def ticketView(request):

    dist = {
        'form':TicketForm()
    }
    noti = notification()
    dist.update(noti)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            aa= form.save(commit=False)
            aa.customer = request.user.customer
            aa.status = 'pending'
            aa.save()
            
            AdminNotification.objects.create(customer = request.user.customer, name ="Created a ticket: "+ aa.subject, types ="ticket", ids=aa.id)
            images = request.FILES.getlist("file[]")
            for img in images:
                image = SupportFile(file=img, support = aa)
                image.save()
            messages.success(request, "Successfully created ticket")
            return HttpResponseRedirect(reverse('customer:ticketList'))
        else:
            print(form.errors)
            messages.success(request, "Something went wrong")

    return render(request, "customer/ticket.html", dist)

def ticketList(request):
    ticket = Ticket.objects.filter(customer = request.user.customer).order_by('-id')
    check = None
    for i in ticket:
        check = i.id
        break

    dist = {
        'ticket':ticket,
        'check':check,
        'form':ReplyForm()
    }
    noti = notification()
    dist.update(noti)
    if request.method == 'POST':
        form = ReplyForm(request.POST, request.FILES)
        if form.is_valid():
            aa= form.save(commit=False)
            aa.replied_by = request.user
            aa.save()
            images = request.FILES.getlist("file[]")
            AdminNotification.objects.create(customer =request.user.customer, name ='Replied to ticket: ' +aa.ticket.subject, types ="ticket", ids=aa.ticket.id)
            for img in images:
                image = SupportFile(file=img, customer = request.user.customer)
                image.save()
            messages.success(request, "Successfully replied ticket")
            return HttpResponseRedirect(reverse('customer:ticketList'))
        else:
            print(form.errors)
            messages.success(request, "Something went wrong")
    return render(request, "customer/ticketList.html", dist)


def defaultCurrencyView(request):
    dist = {
        'currency':Currency.objects.all()
    }
    noti = notification()
    dist.update(noti)
    if request.method == "POST":
        currency = Currency.objects.get(id = request.POST['currency']) 
        try:
            aa = request.user.customer.customer_currency
            aa.currency = currency
            aa.save()
            messages.success(request, "Successfully updated Default Currency")
        except:
           DefaultCurrency.objects.create(customer = request.user.customer, currency = currency)
           messages.success(request, "Successfully Added Default Currency") 
    return render(request, "customer/default_currency.html", dist)


def TwoFactorView(request):
    return render(request, "customer/2fa.html")

def bankView(request):
    bank = BankAccount.objects.filter(customer = request.user.customer).order_by('-id')
    form = BankForm()
    recipient = Recipient.objects.filter(customer = request.user.customer).order_by('-id')
    dist = {
        'bank':bank,
        'form':form,
        'recipient':recipient
    }
    noti = notification()
    dist.update(noti)
    if request.method == 'POST':
        form = BankForm(request.POST)

        if form.is_valid():
            recp = request.POST['recipient']
            aa = form.save(commit= False)
            aa.customer = request.user.customer
            aa.recipient = Recipient.objects.get(id = recp)
            aa.save()
            messages.success(request, "Successfully Added Bank Account")
            return HttpResponseRedirect(reverse('customer:bank'))
        else:
            messages.error(request, "Something went wrong")
    return render(request, "customer/bank.html", dist)



def editBank(request, id):
    
    rec = BankAccount.objects.get(id = id)
    form = BankForm(instance=rec)
    recipient = Recipient.objects.filter(customer = request.user.customer)
    dist = {
        'recipient':recipient,
        'form':form,
        'bank':rec
    }
    noti = notification()
    dist.update(noti)
    if request.method == 'POST':
        form = BankForm(request.POST, instance=rec)
        if form.is_valid():
            sav = form.save(commit=False)
            sav.customer = request.user.customer
            sav.save()
            messages.success(request, "Successfully updated bank details")
            return HttpResponseRedirect(reverse('customer:bank'))
        else:
            messages.error(request,"Something went wrong")
        
    return render(request, "customer/editBank.html", dist)

def deleteBank(request, id):
    bank = BankAccount.objects.get(id = id)
    bank.delete()
    messages.success(request, "Successfully Deleted Bank")
    return HttpResponseRedirect(reverse('customer:bank'))


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



def findBank(request):
    from django.forms.models import model_to_dict
    if request.method == 'POST':
        my_data = request.POST.get('id')  # Get the sent data
        currency = Recipient.objects.get(id = int(my_data))
        print(currency)
        # Process the data and prepare the response
        bank= BankAccount.objects.filter(recipient = currency)
        res = serializers.serialize('json', bank)
    
        return JsonResponse(res, safe=False)  # Return the response as JSON


# Create your views here.
def customerDashboard(request):
    dist = {
        'currency' : Currency.objects.all().order_by('-id')[:3],
        'transaction': Transaction.objects.filter(customer = request.user.customer)[:4]
    }
    noti = notification()
    dist.update(noti)
    return render(request, "customer/dashboard.html", dist)

def recipient(request):
    
    recipient = Recipient.objects.filter(customer = request.user.customer).order_by('-id')
    dist = {
        'recipient':recipient
    }
    noti = notification()
    dist.update(noti)
    return render(request, "customer/recipient.html", dist)



def addRecipient(request):
    form = RecipientForm()
    recipient = Recipient.objects.filter(customer__admin = request.user).order_by('-id')
    dist = {
        'recipient':recipient,
        'form':form
    }
    noti = notification()
    dist.update(noti)
    if request.method == 'POST':
        form = RecipientForm(request.POST)
        if form.is_valid():
            sav = form.save(commit=False)
            sav.customer = request.user.customer
            sav.save()
      
            messages.success(request, "Successfully added recipient")
            return HttpResponseRedirect(reverse('customer:recipient'))
        else:
              
            print(form.errors)
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
    noti = notification()
    dist.update(noti)
    if request.method == 'POST':
        form = RecipientForm(request.POST, instance=rec)
        if form.is_valid():
            sav = form.save(commit=False)
            sav.customer = request.user.customer
            sav.save()
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
    try:
        default = request.user.customer.customer_currency.currency
    except:
        default = Currency.objects.last()

    dist = {
        'recp':Recipient.objects.filter(customer__admin = request.user),
        'currency':Currency.objects.all().exclude(id = default.id),
        'default':default,
        'form':TransactionForm(),
        'customer':request.user.customer
    }
    noti = notification()
    dist.update(noti)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            aa = form.save(commit= False)
            aa.customer = request.user.customer
            aa.save()
            AdminNotification.objects.create(customer =request.user.customer, name ="Transanction Made" , types ="transaction", ids=aa.id)
            messages.success(request, "Your transaction is added and is in pending. You will get notified afer your payment is made")
            return HttpResponseRedirect(reverse('customer:completePayment'))
    return render(request, "customer/sendMoney.html", dist)

def completePayment(request):
    return render(request, "customer/complete.html")

def transactionView(request):
    transaction = Transaction.objects.filter(customer = request.user.customer)

    dist = {
        'transaction':transaction
    }
    noti = notification()
    dist.update(noti)
    return render(request, "customer/transaction.html", dist)

def currency(request):
    currency = Currency.objects.all().order_by('-id')

    dist ={
        'currency':currency
    }
    noti = notification()
    dist.update(noti)
    return render(request, "customer/currency.html", dist)

def kycVerify(request):

    form = KYCForm()
    
    cm = KYC.objects.filter(customer__admin = request.user)
  
    for i in cm:
        cm=i
        break
    if cm:
        form = KYCForm(instance=cm)
    else:
        form = KYCForm()

    if request.user.customer.state:
        form.fields['state'].initial = request.user.customer.state

    if request.user.customer.state:
        form.fields['city'].initial = request.user.customer.city

    if request.user.customer.state:
        form.fields['zip_code'].initial = request.user.customer.zip_code

    if request.user.customer.state:
        form.fields['number'].initial = request.user.customer.number

    if request.user.customer.state:
        form.fields['address'].initial = request.user.customer.address
    
    if request.user.customer.state:
        form.fields['country'].initial = request.user.customer.country 

    dist = {
        'form':form,
        'cm':cm
    }
    noti = notification()
    dist.update(noti)
    if request.method == 'POST':
        if cm:
            form = KYCForm(request.POST, request.FILES, instance=cm)
        else:
            form = KYCForm(request.POST, request.FILES)

       
        if form.is_valid():
            aa = form.save(commit=False)
            aa.customer = request.user.customer
            aa.save()
            AdminNotification.objects.create(customer =request.user.customer, name ="Applied for kyc verification" , types ="kyc", ids=aa.id)
            messages.success(request, "Successfully sent for verification")
            return HttpResponseRedirect(reverse('customer:verify'))
        else:
            print(form.errors)
            dist.update({'form':form})
            messages.success(request, "Something went wrong! " )

    return render(request, "customer/verify.html", dist)


class Profile(View):
    template_name = 'customer/profile.html'
    def get(self, request, *args, **kwargs):
        pcform = PasswordChangeFormUpdate(request.user)
        form = CustomerForm(instance=request.user.customer)
        
        dist = {
            'pcform':pcform,
            'form':form,
            'transaction':Transaction.objects.filter(customer = request.user.customer).order_by('-id')[:5],
            'recipient': Recipient.objects.filter(customer = request.user.customer).order_by('-id')[:5],
            'real_customer':request.user.customer
              
        }
        noti = notification()
        dist.update(noti)
        return render(request, self.template_name, dist)

    def post(self, request, *args, **kwargs):
        real_customer = request.user.customer
        try:
            real_customer.admin.first_name = request.POST['first_name']
            real_customer.admin.last_name = request.POST['last_name']
            real_customer.admin.email = request.POST['email']
            real_customer.admin.username = request.POST['email']
            real_customer.admin.save()
        except:
            messages.error(request, "Email is added already..")
            return HttpResponseRedirect(reverse('customer:profile'))
        form = CustomerForm(request.POST)
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
            return HttpResponseRedirect(reverse('customer:profile'))
        else:
            err = form.errors
            print(err)
            dist = {
            'pcform':PasswordChangeFormUpdate(request.user),
            'form':form,
            'transaction':Transaction.objects.filter(customer = request.user.customer).order_by('-id')[:5],
            'recipient': Recipient.objects.filter(customer = request.user.customer).order_by('-id')[:5],
            'real_customer':request.user.customer            
            }
            noti = notification()
            dist.update(noti)
            messages.error(request, "Something went wrong")
            return render(request, self.template_name, dist)
        
        # return HttpResponseRedirect(reverse('customer:profile'))
    
def GoogleOtpView(request):
    cust = request.user.customer
    if cust.security == "sms":
        cust.security = 'both'
        cust.save()
    else:
        cust.security = 'email'
        cust.save()
    messages.success(request, "Successfully added gmail security")
    return HttpResponseRedirect(reverse('customer:twoFactor'))


def phoneOtpView(request):
    cust = request.user.customer
    if cust.security == "email":
        cust.security = 'both'
        cust.save()
    else:
        cust.security = 'sms'
        cust.save()
    messages.success(request, "Successfully added gmail security")
    return HttpResponseRedirect(reverse('customer:twoFactor'))

def updatePic(request):
    file = request.FILES['profile']
    cust = request.user.customer
    cust.profil_pic = file
    cust.save()
    messages.success(request, "Successfully updated profile picture")
    return HttpResponseRedirect(reverse('customer:profile'))

def disablesms(request):
    cust = request.user.customer
    if cust.security == "both":
        cust.security = 'email'
        cust.save()
    else:
        cust.security = 'none'
        cust.save()
    messages.success(request, "Successfully disabled sms security")
    return HttpResponseRedirect(reverse('customer:twoFactor'))

def disablegmail(request):
    cust = request.user.customer
    if cust.security == "both":
        cust.security = 'sms'
        cust.save()
    else:
        cust.security = 'none'
        cust.save()
    messages.success(request, "Successfully disabled gmail security")
    return HttpResponseRedirect(reverse('customer:twoFactor'))

