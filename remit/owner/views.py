from django.db.models.aggregates import Sum
import datetime
from django.shortcuts import render
from django.views.generic import View, UpdateView
from homepage.models import Feature, Service, Client, Testomonial, Footor, Brand, AboutUs, ChooseUs, HomeService
from homepage.models import CompanyInformation, CustomUser, SendingPurpose, SourceFund
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from homepage.models import Blog, AdminBankAccount, Customer, Restriction, Agent, Owner, LoginInterface, signupInterface, Policy, Terms, SocialLink

from homepage.models import Country, Currency, Recipient, PickupPoint, KYC, Transaction, BankAccount
from .models import SiteSetting, SEO, BlockPlace
from .forms import SiteForm, SEOForm, FeatureForm, AboutForm, HomeServiceForm, ChooseForm, CountryForm, CurrencyForm, RecipientForm, PickupPointForm, KYCForm
from homepage.forms import CustomerForm, AgentForm, PasswordChangeFormUpdate, ReplyForm, TicketForm

from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from homepage.models import  DefaultCurrencyAdmin, EmailSetting, SMSSetting, EmailList, SMSList, DefaultNumber, Ticket, SupportFile, AdminNotification, CustomerNotification
from homepage.forms import AdminBankForm, BankForm, RestrictionForm, UserCreateForm, UserUpdateForm, ServiceForm, ClientForm, TestomonialForm, CompanyInformationForm, BlogForm, CategoryForm, SubCategoryForm

from .forms import BlockForm, PurposeForm, FundForm, DefaultForm, EmailSettingForm, SMSSettingForm, LoginInterfaceForm, signupInterfaceForm, AboutForm, SEOForm, BrandForm, FootorForm, SocialForm, PolicyForm, TermForm, EmailListForm, SMSListForm
from django.http import JsonResponse
from homepage.models import LoginLogs, TransactionNote

from django.core.mail import send_mail, BadHeaderError
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from owner.models import SiteSetting
from django.conf import settings
from customer.twilio import TwilioOTPSMS
# Create your views here.


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

def deleteAdminBank(request, id):
    bank = AdminBankAccount.objects.get(id = id)
    bank.delete()
    messages.success(request, "Successfully Deleted Bank")
    return HttpResponseRedirect(reverse('owner:bank'))


def editAdminBank(request, id):
    
    rec = AdminBankAccount.objects.get(id = id)
    form = AdminBankForm(instance=rec)
   
    dist = {
        'form':form,
        'bank':rec
    }
    noti = notification(request)
    dist.update(noti)
    if request.method == 'POST':
        form = AdminBankForm(request.POST, instance=rec)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated bank details")
            return HttpResponseRedirect(reverse('owner:bank'))
        else:
            messages.error(request,"Something went wrong")
        
    return render(request, "owner/editAdminBank.html", dist)

def defaultCurrency(request):
   
    asa = DefaultCurrencyAdmin.objects.all()
    if asa:
        for i in asa:
            asa = i
            break

    dist = {
        'currency':Currency.objects.all(),
        'default_currency':asa
    }
    noti = notification(request)
    dist.update(noti)
    if request.method == "POST":
        currency_s = Currency.objects.get(id = request.POST['send_currency']) 
        currency_r = Currency.objects.get(id = request.POST['receive_currency']) 
        try:
            asa.sending_currency = currency_s
            asa.receiving_currency = currency_r
            asa.save()

            messages.success(request, "Successfully updated Default Currency")
        except:
           DefaultCurrencyAdmin.objects.create(sending_currency = currency_s, receiving_currency= currency_r )
           messages.success(request, "Successfully Added Default Currency") 
           return HttpResponseRedirect(reverse('owner:default'))
    # return render(request, "customer/default_currency.html", dist)
    return render(request, "owner/default.html", dist)

def search(request):
    query = request.GET.get('search')

    bank = BankAccount.objects.filter(account_name__icontains=query)
    currency = Currency.objects.filter(country__name__icontains=query)
    country = Country.objects.filter(name__icontains=query)
    agent = CustomUser.objects.filter(first_name__icontains=query).filter(user_type = "customer")
    customer = CustomUser.objects.filter(first_name__icontains=query).filter(user_type = "agent")
    dist = {
        'country':country,
        'bank':bank,
        'customer':customer,
        'agent':agent,
        'currency':currency,
        'noti': AdminNotification.objects.filter(seen= False),
        'noti_count' : AdminNotification.objects.filter(seen= False).count(),
    }
    return render(request, 'owner/search.html', dist)


def seenNotification(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print(id)  
        tic = AdminNotification.objects.get(id = int(id))

        tic.seen = True
        tic.save()
        return JsonResponse({'staus':'ok'})

def allRead(request):
    tic = AdminNotification.objects.filter(seen = False)
    for i in tic:
        i.seen = True
        i.save()
    return HttpResponseRedirect(reverse('owner:allNotification'))

def notification(request):
    noti = AdminNotification.objects.filter(seen= False).order_by('-id')
    count = noti.filter(seen= False).count()
    try:
       navbarstatus= request.session['navbar']
    except:
        navbarstatus= 'big'
    li = {
        'noti':noti,
        'noti_count':count,
        'navbarstatus':navbarstatus
    }
    return li


def allNotification(request):
    noti = AdminNotification.objects.all().order_by('-id')
    count = noti.filter(seen= False).count()
    try:
       navbarstatus= request.session['navbar']
    except:
        navbarstatus= 'big'
    dist = {
        'noti':noti,
        'noti_count':count,
        'navbarstatus':navbarstatus
    }

    return render(request, "owner/notification.html", dist)


def transactionView(request):
    trans = Transaction.objects.all().order_by('-id')
    total_t = trans.count()
    rejected = trans.filter(status = "Rejected").count()
    pending = trans.filter(status = "Pending").count()
    complete = trans.filter(status = "Completed").count()
    cancelled = trans.filter(status = "Cancelled").count()
    today_trans = trans.filter(created_at__date = datetime.date.today()).count()
    total_cost = trans.aggregate(sum_amount=Sum('sent'))['sum_amount']
    today_total = Transaction.objects.filter(created_at__date = datetime.date.today()).aggregate(sum_amount=Sum('sent'))['sum_amount']
    dist = {
        'total_cost':total_cost,
        'fees':trans.aggregate(sum_amount=Sum('fee'))['sum_amount'],
        'today_cost':today_total if today_total else 0,
        'today_trans':today_trans,
        'transaction':trans, 'total_t':total_t,
        'rejected':rejected,
        'pending':pending,
        'complete':complete,
        'cancelled':cancelled,
        'transCancelled':trans.filter(status= "Cancelled"),
        'transRejected':trans.filter(status= "Rejected"),
        'transComplete':trans.filter(status= "Completed"),
        'transPending':trans.filter(status= "Pending"),

    }
    noti = notification(request)
    dist.update(noti)

    return render(request, "owner/transaction.html", dist)

def transactionDetail(request, id):
    trans = Transaction.objects.get(id = id)
    alltrans = Transaction.objects.filter(customer = trans.customer)
    dist = {
        'trans':trans,
        'alltrans':alltrans
    }
    noti = notification(request)
    dist.update(noti)

    return render(request, 'owner/transactionDetail.html', dist)


def banCustomer(request, id):
    customer = Customer.objects.get(id = id)
    customer.banned = True
    customer.save()
    messages.success(request ,"Successfully Banned Customer")
    return HttpResponseRedirect(reverse('owner:customerProfile', args=[customer.admin.id]))

def banCustomerDisable(request, id):
    customer = Customer.objects.get(id = id)
    customer.banned = False
    customer.save()
    messages.success(request ,"Successfully Allowed banned Customer")
    return HttpResponseRedirect(reverse('owner:customerProfile', args=[customer.admin.id]))



# EMAIL AND SMS
def emailSetting(request):
    email = EmailSetting.objects.all()
    form = EmailSettingForm()
    if email:
        for i in email:
            email = i
            form = EmailSettingForm(instance=i)
            break
    dist = {
        'form': form,
        'email':email,
        'all_email':EmailList.objects.all().order_by('-id'),
        'customer':Customer.objects.all().order_by('-id'),
        'agent':Agent.objects.all().order_by('-id'),
        'recipient': Recipient.objects.all().order_by('-id'),
        'sendform':EmailListForm()
    }

    if request.method == 'POST':
        sendform = EmailListForm(request.POST)
        recipient_list = []
        if sendform.is_valid():
            aa = sendform.save()
            content = settings.EMAIL_HOST_USER
            sub = aa.subject
            messa = aa.message
            try:
                us = Customer.objects.get(id = request.POST['customer'])
                recipient_list = [us.admin.email, ]
            except:
                pass

            try:
                us = Agent.objects.get(id = request.POST['agent'])
                recipient_list = [us.admin.email, ]
                
            except:
                pass
            try:
                us = Recipient.objects.get(id = request.POST['reciptient'])
                recipient_list = [us.email, ]
                
            except:
                pass
      
            us = request.POST['group']
            if us == 'Customer':
                recipient_list = []
                allCustomer = Customer.objects.all()
                for i in allCustomer:
                    try:
                        recipient_list.append(i.admin.email)
                    except:
                        pass

            if us == 'Agent':
                allCustomer = Agent.objects.all()
                for i in allCustomer:
                    try:
                        recipient_list.append(i.admin.email)
                    except:
                        pass

            if us == 'Recipient':
                allCustomer = Recipient.objects.all()
                for i in allCustomer:
                    try:
                        recipient_list.append(i.email)
                    except:
                        pass
           
            print(us)
            print(recipient_list)
            content = settings.EMAIL_HOST_USER

            other_info = siteInfo()
            
           
            dist_info = {
                'sub': sub, 'message':strip_tags(messa),
            }
            dist_info.update(other_info)
            html_message = render_to_string('component/email.html', dist_info)
            pain_html_msg = strip_tags(html_message)
            # try: 
            msg = EmailMultiAlternatives(sub, pain_html_msg, content, recipient_list)
            msg.attach_alternative(html_message, "text/html")
            msg.send()
            messages.success(request,"Successfully send email.")
            # except:
            #     messages.error(request,"Failed to sent email. Please ask to verify customer email")    
                
            return HttpResponseRedirect(reverse('owner:emailSetting'))
        else:
            print(sendform.errors)
            dist.update({'sendform':sendform})
            messages.error(request, "something went wrong")

    noti = notification(request)
    dist.update(noti)
   
    return render(request, "owner/email.html", dist)

def addEmailSetting(request, id):
    if id == 0:
        form = EmailSettingForm(request.POST)
    else:
        instance = EmailSetting.objects.get(id = id)
        form = EmailSettingForm(request.POST, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, "Successfully updated email settings")
        return HttpResponseRedirect(reverse('owner:emailSetting'))
    else:
        
        dist = {
            'form': form
        }

        noti = notification(request)
        dist.update(noti)

        messages.error(request, "Something went wrong")
        return render(request, "owner/email.html", dist)    

def smsSetting(request):
    email = SMSSetting.objects.all()
    form = SMSSettingForm()
    defautForm = DefaultForm()
    if email:
        for i in email:
            email = i
            form = SMSSettingForm(instance=i)
            break
    defs = DefaultNumber.objects.first()
    if defs:
        defautForm.fields['number'].initial = defs.number
    dist = {
        'form': form,
        'email':email,
        'all_email':SMSList.objects.all().order_by('-id'),
        'customer':Customer.objects.all().order_by('-id'),
        'agent':Agent.objects.all().order_by('-id'),
        'recipient': Recipient.objects.all().order_by('-id'),
        'sendform':SMSListForm(),
        'defautForm':defautForm,
        'defs':defs
    }
    noti = notification(request)
    dist.update(noti)

    if request.method == 'POST':
        sendform = SMSListForm(request.POST)
        
        if sendform.is_valid():
            aa = sendform.save()
        
            messa = aa.message
            try:
                us = Customer.objects.get(id = request.POST['customer'])
                TwilioOTPSMS(messa, us.number)
            except:
                pass

            try:
                us = Agent.objects.get(id = request.POST['agent'])
                TwilioOTPSMS(messa, us.number)
                
            except:
                pass
            try:
                us = Recipient.objects.get(id = request.POST['reciptient'])
                TwilioOTPSMS(messa, us.number)
              
                
            except:
                pass
      
            us = request.POST['group']
            print(us)
            if us == 'Customer':
                allCustomer = Customer.objects.all()
                for i in allCustomer:
                    try:
                        TwilioOTPSMS(messa, i.number)
                    except:
                        pass

            if us == 'Agent':
                allCustomer = Agent.objects.all()
                for i in allCustomer:
                    try:
                        TwilioOTPSMS(messa, i.number)
                    except:
                        pass

            if us == 'Recipient':
                allCustomer = Recipient.objects.all()
                for i in allCustomer:
                    try:
                        TwilioOTPSMS(messa, i.number)
                    except:
                        pass
           
          
           
            messages.success(request, 'Successfully sent sms')
            return HttpResponseRedirect(reverse('owner:smsSetting'))
        else:
            print(sendform.errors)
            dist.update({'sendform':sendform})
            messages.error(request, "something went wrong")

    return render(request, "owner/sms.html", dist)

def addDefaultNumber(request):
    form = DefaultForm(request.POST)

    if form.is_valid():
        form.save()
        messages.success(request, "Successfully added new number")
        return HttpResponseRedirect(reverse('owner:smsSetting'))
    else:
        messages.error(request, "Something went wrong")
        return HttpResponseRedirect(reverse('owner:smsSetting'))
    
def updateDefaultNumber(request, id):
    form = DefaultForm(request.POST, instance = DefaultNumber.objects.get(id = id))

    if form.is_valid():
        form.save()
        messages.success(request, "Successfully updated number")
        return HttpResponseRedirect(reverse('owner:smsSetting'))
    else:
        messages.error(request, "Something went wrong")
        return HttpResponseRedirect(reverse('owner:smsSetting'))
    
def addSMSSetting(request):
 
    form = SMSSettingForm(request.POST)
    
    if form.is_valid():
        form.save()
        messages.success(request, "Successfully added SMS settings")
        return HttpResponseRedirect(reverse('owner:smsSetting'))
    else:
        
        dist = {
            'form': form
        }

        noti = notification(request)
        dist.update(noti)

        messages.error(request, "Something went wrong")
        return render(request, "owner/sms.html", dist) 

def updateSMSSetting(request, id):

    instance = SMSSetting.objects.get(id = id)
    form = SMSSettingForm(request.POST, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, "Successfully updated SMS settings")
        return HttpResponseRedirect(reverse('owner:smsSetting'))

    dist = {
        'form': form
    }

    noti = notification(request)
    dist.update(noti)

    messages.error(request, "Something went wrong")
    return render(request, "owner/sms.html", dist) 

# BANNED USER

def bannedSetting(request):
    banned = Customer.objects.filter(banned = True)

    dist = {
        'banned':banned
    }

    noti = notification(request)
    dist.update(noti)
    return render(request, "owner/banned.html", dist)



# Bank Information
def bankView(request):
    bank = BankAccount.objects.all().order_by('-id')
    total_bank = bank.count()
    form = AdminBankForm()
    customer = Customer.objects.all().order_by('-id')
    Adminbank = AdminBankAccount.objects.all().order_by('-id')
    dist = {
        'bank':bank,
        'form':form,
        'customer':customer,
        'total_bank':total_bank,
        'Adminbank':Adminbank,
    }
    noti = notification(request)
    dist.update(noti)
    if request.method == 'POST':
        form = AdminBankForm(request.POST)
        if form.is_valid():
            sav = form.save(commit=False)
            sav.save()
            messages.success(request, "Successfully add bank details")
            return HttpResponseRedirect(reverse('owner:bank'))
        else:
            messages.error(request,"Something went wrong")
  
    return render(request, "owner/bank.html", dist)



def editBank(request, id):
    
    rec = BankAccount.objects.get(id = id)
    form = BankForm(instance=rec)
    recipient = Recipient.objects.filter(customer = rec.customer)
    dist = {
        'recipient':recipient,
        'form':form,
        'bank':rec
    }
    noti = notification(request)
    dist.update(noti)
    if request.method == 'POST':
        form = BankForm(request.POST, instance=rec)
        if form.is_valid():
            form.save()
          
            # sav.save()
            messages.success(request, "Successfully updated bank details")
            return HttpResponseRedirect(reverse('owner:bank'))
        else:
            messages.error(request,"Something went wrong")
        
    return render(request, "owner/editBank.html", dist)


def deleteBank(request, id):
    bank = BankAccount.objects.get(id = id)
    bank.delete()
    messages.success(request, "Successfully Deleted Bank")
    return HttpResponseRedirect(reverse('owner:bank'))

def filterBank(request):
    idS = request.GET['customer']
    print(idS)
    bank = BankAccount.objects.filter(customer_id = idS ).order_by('-id')
    total_bank = bank.count()
    form = AdminBankForm()
    customer = Customer.objects.all().order_by('-id')
    Adminbank = AdminBankAccount.objects.all().order_by('-id')
    dist = {
        'cust_id':idS,
        'bank':bank,
        'form':form,
        'Adminbank':Adminbank,
        'customer':customer,
        'total_bank':total_bank,
        'recipient':Recipient.objects.all()
    }
    noti = notification(request)
    dist.update(noti)
    if request.method == 'POST':
        form = AdminBankForm(request.POST)
        if form.is_valid():
            sav = form.save(commit=False)
            sav.save()
            messages.success(request, "Successfully add bank details")
            return HttpResponseRedirect(reverse('owner:bank'))
        else:
            messages.error(request,"Something went wrong")
    return render(request, "owner/bank.html", dist)



def deleteBank(request, id):
    bank = BankAccount.objects.get(id = id)
    bank.delete()
    messages.success(request, "Successfully Deleted Bank")
    return HttpResponseRedirect(reverse('owner:bank'))


# Blog Information
def blogView(request):
    bank = Blog.objects.all().order_by('-id')
    total_bank = bank.count()
    form = BlogForm()
    
    dist = {
        'blog':bank,
        'form':form,
        'total_blog':total_bank,
       
    }
    noti = notification(request)
    dist.update(noti)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)

        if form.is_valid():
            
            form.save()
            messages.success(request, "Successfully Added New Blog")
            return HttpResponseRedirect(reverse('owner:blog'))
        else:
            messages.error(request, "Something went wrong")
    return render(request, "owner/blog.html", dist)

def editBlog(request, id):
    
    rec = Blog.objects.get(id = id)
    form = BlogForm(instance=rec)
   
    dist = {
        'form':form,
        'blog':rec,
        'total_blog':Blog.objects.all().count()
    }
    noti = notification(request)
    dist.update(noti)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=rec)
        if form.is_valid():
            form.save()
           
            messages.success(request, "Successfully updated blog details")
            return HttpResponseRedirect(reverse('owner:blog'))
        else:
            messages.error(request,"Something went wrong")
        
    return render(request, "owner/editBlog.html", dist)

def deleteBlog(request, id):
    bank = Blog.objects.get(id = id)
    bank.delete()
    messages.success(request, "Successfully Deleted Blog")
    return HttpResponseRedirect(reverse('owner:blog'))


def ticketList(request):
    ticket = Ticket.objects.all().order_by('-id')
    check = None
    for i in ticket:
        check = i.id
        break

    dist = {
        'ticket':ticket,
        'check':check,
        'form':ReplyForm()
    }
    noti = notification(request)
    dist.update(noti)
   
    return render(request, "owner/ticket.html", dist)

def replyTicket(request, id):
    if request.method == 'POST':
        form = ReplyForm(request.POST, request.FILES)
        if form.is_valid():

            aa= form.save(commit=False)
            aa.replied_by = request.user
            aa.ticket = Ticket.objects.get(id = id)
            aa.save()
            tick = Ticket.objects.get(id = id)
            tick.ticket = tick
            tick.status = "answered"
            tick.save()
            CustomerNotification.objects.create(customer =tick.customer, name ='Replied to ticket: ' +tick.subject, types ="ticket", ids=tick.id)
            
            messages.success(request, "Successfully replied ticket")
            return HttpResponseRedirect(reverse('owner:ticketView'))
        else:
            print(form.errors)
            messages.success(request, "Something went wrong")
    return HttpResponseRedirect(reverse('owner:ticketView'))

def closeTicket(request, id):
    tock = Ticket.objects.get(id = id)
    tock.status = 'closed'
    tock.save()
    messages.success(request, "Successfully closed ticket")
    return HttpResponseRedirect(reverse('owner:ticketView'))

def changeStatus(request, id):
    status = request.POST['status']
    trans = Transaction.objects.get(id = id)
    trans.status = status
    trans.save()
    CustomerNotification.objects.create(customer = trans.customer, name =str(trans.status), types ="transaction", ids=trans.id)
    content = settings.EMAIL_HOST_USER
    
    if trans.status == 'Completed':
        sub = 'Successfully completed a Transaction Syon Remit'
        messa = "Your transaction is completed successfully."
    elif trans.status == 'Cancelled':
        sub = 'Your transaction is cancelled'
        messa = "Your transaction is completed cancelled."
    elif trans.status == 'Rejected':
        sub = 'Your transaction is rejected'
        messa = "We are sorry to inform you that your transaction is rejected"
    else:
        sub = 'Your transaction is still in pending'
        messa = "We are sorry to inform you that your transaction is still in pending. It may takes few days more to complete your transaction."
    other_info = siteInfo()
    
    recipient_list = [trans.customer.admin.email]
    dist_info = {
        'sub': sub, 'message':messa, 'trans':trans
    }
    dist_info.update(other_info)
    html_message = render_to_string('component/transaction.html', dist_info)
    pain_html_msg = strip_tags(html_message)
    try: 
        msg = EmailMultiAlternatives(sub, pain_html_msg, content, recipient_list)
        msg.attach_alternative(html_message, "text/html")
        msg.send()
    except:
        messages.error(request,"Transaction completed. However failed to sent email. Please ask to verify customer email")
   
    return HttpResponseRedirect(reverse('owner:transactionDetail', args=[trans.id]))

class Dashboard(View):
    template_name = "owner/dashboard.html"
    def get(self, request, *args, **kwargs, ):
        restrict = Restriction.objects.all()
        restrictForm = RestrictionForm()
        if restrict:
            for i in restrict:
                restrict = i
                restrictForm = RestrictionForm(instance=i)
                break
        blog = Blog.objects.all()[:4]

        dist = {
            'restrict':restrict,
            'blog':blog,
            'form':restrictForm,
            'transaction': Transaction.objects.all().order_by('-id')[:5]
        }
        blog_count = Blog.objects.all().count()
        staff_count = CustomUser.objects.all().count()
        client_count = Client.objects.all().count()
        # product_count = Product.objects.all().count()
        service_count = Service.objects.all().count()
        testo_count = Testomonial.objects.all().count()

        public = {
            'blog_count':blog_count,
            'staff':staff_count,
            'client_count':client_count,
            # 'product':product_count,
            'service':service_count,
            'testo_count':testo_count,
            'user':CustomUser.objects.filter(user_type = "customer")
        }

        dist.update(public)
        noti = notification(request)
        dist.update(noti)


       
        restriction = Restriction.objects.first()
    
        try:
            default = Currency.objects.first()
        except:
            default = Currency.objects.last()
       
        nexts = {
            'recp':Recipient.objects.filter(customer__admin = request.user),
            'restriction':restriction,
            'default':default,
        }
        dist.update(nexts)

        return render(request, self.template_name, dist)
    

def addRestriction(request, id):
    if id == 0:
        form = RestrictionForm(request.POST)
    else:
        instance = Restriction.objects.get(id = id)
        form = RestrictionForm(request.POST, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, "Successfully updated restriction settings")
        return HttpResponseRedirect(reverse('owner:dashboard'))
    else:
        
        dist = {
            'form': form
        }

        noti = notification(request)
        dist.update(noti)

        messages.error(request, "Something went wrong")
        return HttpResponseRedirect(reverse('owner:dashboard'))    

# Add Customer
class CustomerView(View):
    template_name = 'owner/customer.html'
    dist = {
            'form':CustomerForm(),
            'form_head': "Add new customer",
            'button':"Add new customer",
            'user': CustomUser.objects.filter(user_type = "customer").order_by('-id')
        }
   
    def get(self, request, *args, **kwargs):
        noti = notification(request)
        self.dist.update(noti)
        return render(request, self.template_name, self.dist)
    def post(self, request, *args, **kwars):
        form = CustomerForm(request.POST)
        # try:
        # custom_user = 
        if form.is_valid():
            try:
                admin = CustomUser.objects.create_user(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], username = request.POST['email'], password = request.POST['password'], user_type = 'customer')

                obj = admin.customer
                obj.number = request.POST['number']
                obj.mail_address = request.POST['mail_address']
                obj.state = request.POST['state']
                obj.city = request.POST['city']
                obj.country = request.POST['country']
                obj.address = request.POST['address']
                obj.added_by = request.user
                obj.save()
                 # admin.save()
                messages.success(request, "Successfully Added Customer")
                return HttpResponseRedirect(reverse('owner:customer'))
            except:      
                messages.error(request, "Email already exist")
                return render(request, self.template_name, self.dist)
        else:
            error = form.errors()
            print(error)
            messages.error(request, str(error))
            return render(request, self.template_name, self.dist)


def deleteCustomer(request, id):
    cust = CustomUser.objects.get(id = id)
    cust.delete()
    messages.success(request, "Successfully delete customer")
    return HttpResponseRedirect(reverse('owner:customer'))


def customerProfile(request, id):
    real_customer = CustomUser.objects.get(id = id)
    cm = KYC.objects.filter(customer=real_customer.customer)
  
    for i in cm:
        cm=i
        break

    form = CustomerForm(instance=real_customer.customer)
    print(BankAccount.objects.filter(customer = real_customer.customer).order_by('-id'))
    dist = {
        'real_customer':real_customer,
        'form':form,
        'form_head':"Update Customer",
        'button':"Update customer",
        'cm':cm,
        'reciepient': Recipient.objects.filter(customer = real_customer.customer).order_by('-id'),
        'transaction': Transaction.objects.filter(customer = real_customer.customer).order_by('-id'),
        'bankA': BankAccount.objects.filter(customer = real_customer.customer).order_by('-id'),
        'login_log' : LoginLogs.objects.filter(customer =real_customer.customer)
    
    }
    noti = notification(request)
    dist.update(noti)
    if request.method == 'POST':
        try: 
            real_customer.first_name = request.POST['first_name']
            real_customer.last_name = request.POST['last_name']
            real_customer.email = request.POST['email']
            real_customer.username = request.POST['email']
            real_customer.save()
        except:
            messages.error(request, "Email is added already..")
            return HttpResponseRedirect(reverse('owner:customerProfile',args=[real_customer.id]))
        form = CustomerForm(request.POST)
        if form.is_valid():
            
            real_customer.customer.number = request.POST['number']
            real_customer.customer.mail_address = request.POST['mail_address']
            real_customer.customer.state = request.POST['state']
           
            real_customer.customer.city = request.POST['city']
            real_customer.customer.country= request.POST['country']
            real_customer.customer.address = request.POST['address']
            real_customer.customer.save()
            form.save()
            messages.success(request, "Successfully Updated Customer")
            return HttpResponseRedirect(reverse('owner:customerProfile',args=[real_customer.id]))
        else:
            messages.error(request, "Something went wrong")
    return render(request, 'owner/customerProfile.html',dist)
   

# Add Agent
def AgentView(request):
    template_name = 'owner/agent.html'
    dist = {
            'agent_form':AgentForm(),
            'form_head': "Add new agent",
            'button':"Add new agent",
            'agent': CustomUser.objects.filter(user_type = "agent").order_by('-id')
        }
    noti = notification(request)
    dist.update(noti) 
    if request.method == 'POST':
        form = AgentForm(request.POST)
        try:
            if form.is_valid():
                # try:
                admin = CustomUser.objects.create_user(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], username = request.POST['email'], password = request.POST['password'], user_type = 'agent')
                obj = admin.agent
                obj.number = request.POST['number']
                obj.mail_address = request.POST['mail_address']
                obj.state = request.POST['state']
                obj.zip_code = request.POST['zip_code']
                obj.city = request.POST['city']
                obj.country = request.POST['country']
                obj.address = request.POST['address']
                obj.added_by = request.user
                obj.save()
                    # admin.save()
                messages.success(request, "Successfully Added Agent")
                return HttpResponseRedirect(reverse('owner:agent'))
        except:      
                messages.error(request, "Email already exist")
                return render(request, template_name, dist)
        else:
            error = form.errors()
            print(error)
            messages.error(request, str(error))
            return render(request, template_name,dist)
    return render(request, template_name,dist)

def deleteAgent(request, id):
    cust = CustomUser.objects.get(id = id)
    cust.delete()
    messages.success(request, "Successfully delete agent")
    return HttpResponseRedirect(reverse('owner:agent'))


def agentProfile(request, id):
    real_customer = CustomUser.objects.get(id = id)
   
    form = AgentForm(instance=real_customer.agent)
    dist = {
        'real_customer':real_customer,
        'form':form,
        'form_head':"Update Agent",
        'button':"Update Agent",
    }
    noti = notification(request)
    dist.update(noti)
    if request.method == 'POST':
        try: 
            real_customer.first_name = request.POST['first_name']
            real_customer.last_name = request.POST['last_name']
            real_customer.email = request.POST['email']
            real_customer.username = request.POST['email']
            real_customer.save()
        except:
            messages.error(request, "Email is added already..")
            return HttpResponseRedirect(reverse('owner:agentProfile',args=[real_customer.id]))
        form = AgentForm(request.POST)
        if form.is_valid():
            
            real_customer.agent.number = request.POST['number']
            real_customer.agent.mail_address = request.POST['mail_address']
            real_customer.agent.state = request.POST['state']
            real_customer.agent.zip_code = request.POST['zip_code']
            real_customer.agent.city = request.POST['city']
            real_customer.agent.country= Country.objects.get(id = request.POST['country']) 
            real_customer.agent.address = request.POST['address']
            real_customer.agent.save()
            form.save()
            messages.success(request, "Successfully Updated agent")
            return HttpResponseRedirect(reverse('owner:agentProfile',args=[real_customer.id]))
        else:
            messages.error(request, "Something went wrong")
    return render(request, 'owner/agentProfile.html',dist)



# -----------CRUD PRODUCT----------------------->
# Product CRUD
class AddFeature(View):
    template_name = "owner/siteSetting/addFeature.html"

    def get(self, request, *args, **kwargs ):
        form = FeatureForm()
        blog = Feature.objects.all().order_by('-id')
        dist = {
            'form':form,
            'blog':blog,
            'button':'Add Features',
        }
     
        noti = notification(request)
        dist.update(noti)
        return render(request, self.template_name, dist)
    def post(self, request, *args, **kwargs):
        form = FeatureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added Feature")
            return HttpResponseRedirect(reverse('owner:addFeature'))
        else:
            messages.success(request, "Something went Wrong")
            return HttpResponseRedirect(reverse('owner:addFeature'))
  

class UpdateFeature(SuccessMessageMixin, UpdateView):
    template_name = "owner/siteSetting/editFeature.html"
    model = Feature
    form_class = FeatureForm
    success_message = "Successfully Updated Feature"
    
    def get_success_url(self, *args, **kwargs):
        id = self.kwargs['pk']
        return reverse('owner:updateFeature', args=[id])
    
def deleteFeature(request, id):
    blog = Feature.objects.get(id = id)
    blog.delete()
    messages.success(request, "Succesfully Deleted Feature")
    return HttpResponseRedirect(reverse('owner:addFeature')) 




# Crud Brand

class AddBrand(View):
    template_name = "owner/siteSetting/addBrand.html"

    def get(self, request, *args, **kwargs ):
        form = BrandForm()
        blog = Brand.objects.all().order_by('-id')
        dist = {
            'form':form,
            'blog':blog,
            'button':'Add Brands',
        }
     
        noti = notification(request)
        dist.update(noti)
        return render(request, self.template_name, dist)
    def post(self, request, *args, **kwargs):
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added Brand")
            return HttpResponseRedirect(reverse('owner:addBrand'))
        else:
            messages.success(request, "Something went Wrong")
            return HttpResponseRedirect(reverse('owner:addBrand'))
  

class UpdateBrand(SuccessMessageMixin, UpdateView):
    template_name = "owner/siteSetting/editBrand.html"
    model = Brand
    form_class = BrandForm
    success_message = "Successfully Updated Brand"
    
    def get_success_url(self, *args, **kwargs):
        id = self.kwargs['pk']
        return reverse('owner:updateBrand', args=[id])
    
def deleteBrand(request, id):
    blog = Brand.objects.get(id = id)
    blog.delete()
    messages.success(request, "Succesfully Deleted Brand")
    return HttpResponseRedirect(reverse('owner:addBrand'))

# -------------------------------------------->
# CRUD Service -------------------------------->
# -------------------------------------------->
class AddService(View):
    template_name = "owner/service/addService.html"

    def get(self, request, *args, **kwargs ):
        form = ServiceForm()
        blog = Service.objects.all().order_by('-id')
        dist = {
            'form':form,
            'blog':blog,
            'button':'Add Service',
        }
      
        noti = notification(request)
        dist.update(noti)

        return render(request, self.template_name, dist)
    def post(self, request, *args, **kwargs):
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added Service")
            return HttpResponseRedirect(reverse('owner:addService'))
        else:
            messages.success(request, "Something went Wrong")
            return HttpResponseRedirect(reverse('owner:addService'))
  

class UpdateService(SuccessMessageMixin, UpdateView):
    template_name = "owner/service/editService.html"
    model = Service
    form_class = ServiceForm
    success_message = "Successfully Updated Service"
    
    def get_success_url(self, *args, **kwargs):
        id = self.kwargs['pk']
        return reverse('owner:updateService', args=[id])
    

def deleteService(request, id):
    blog = Service.objects.get(id = id)
    blog.delete()
    messages.success(request, "Succesfully Deleted Service")
    return HttpResponseRedirect(reverse('owner:addService')) 







# -------------------------------------------->
# CRUD Client -------------------------------->
# -------------------------------------------->
class AddClient(View):
    template_name = "owner/client/addClient.html"

    def get(self, request, *args, **kwargs ):
        form = ClientForm()
        blog = Client.objects.all().order_by('-id')
        dist = {
            'form':form,
            'blog':blog,
            'button':'Add Client',
        }
       
        noti = notification(request)
        dist.update(noti)
        return render(request, self.template_name, dist)
    def post(self, request, *args, **kwargs):
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added Client")
            return HttpResponseRedirect(reverse('owner:addClient'))
        else:
            messages.success(request, "Something went Wrong")
            return HttpResponseRedirect(reverse('owner:addClient'))
  

class UpdateClient(SuccessMessageMixin, UpdateView):
    template_name = "owner/client/editClient.html"
    model = Client
    form_class = ClientForm
    success_message = "Successfully Updated Client"
    
    def get_success_url(self, *args, **kwargs):
        id = self.kwargs['pk']
        return reverse('owner:updateClient', args=[id])
def deleteClient(request, id):
    blog = Client.objects.get(id = id)
    blog.delete()
    messages.success(request, "Succesfully Deleted Client")
    return HttpResponseRedirect(reverse('owner:addClient')) 






# -------------------------------------------->
# CRUD Testomonial -------------------------------->
# -------------------------------------------->

class AddTestomonial(View):
    template_name = "owner/testomonial/addTestomonial.html"

    def get(self, request, *args, **kwargs ):
        form = TestomonialForm()
        blog = Testomonial.objects.all().order_by('-id')
        dist = {
            'form':form,
            'blog':blog,
            'button':'Add Testomonial',
        }
        noti = notification(request)
        dist.update(noti)

        return render(request, self.template_name, dist)
    def post(self, request, *args, **kwargs):
        form = TestomonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added Testomonial")
            return HttpResponseRedirect(reverse('owner:addTestomonial'))
        else:
            messages.success(request, "Something went Wrong")
            return HttpResponseRedirect(reverse('owner:addTestomonial'))
  

class UpdateTestomonial(SuccessMessageMixin, UpdateView):
    template_name = "owner/testomonial/editTestomonial.html"
    model = Testomonial
    form_class = TestomonialForm
    success_message = "Successfully Updated Testomonial"
    
    def get_success_url(self, *args, **kwargs):
        id = self.kwargs['pk']
        return reverse('owner:updateTestomonial', args=[id])
def deleteTestomonial(request, id):
    blog = Testomonial.objects.get(id = id)
    blog.delete()
    messages.success(request, "Succesfully Deleted Testomonial")
    return HttpResponseRedirect(reverse('owner:addTestomonial')) 



    
# CRUD BLOG
class AddBlog(View):
    template_name = "staff/addBlog.html"

    def get(self, request, *args, **kwargs ):
        form = BlogForm()
        blog = Blog.objects.all().order_by('-id')

       
        dist = {
            'form':form,
            'blog':blog,
            'button':'Add Blog',
        }

        noti = notification(request)
        dist.update(noti)
        return render(request, self.template_name, dist)
    def post(self, request, *args, **kwargs):
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added Blog")
            return HttpResponseRedirect(reverse('owner:addBlog'))
        else:
            messages.success(request, "Something went Wrong")
            return HttpResponseRedirect(reverse('owner:addBlog'))






# Profle Crud>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class Profile(View):
    template_name = 'owner/profile.html'
    def get(self, request, *args, **kwargs):
        form = PasswordChangeFormUpdate(request.user)
        dist = {
            'form':form
        }
        noti = notification(request)
        dist.update(noti)
        return render(request, self.template_name, dist)

    def post(self, request, *args, **kwargs):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
    
        adm = request.user
        adm.first_name = first_name
        adm.last_name = last_name
        adm.email = email
        try:
            adm.save()
            messages.success(request, "Sucessfully Updated Profile")
        except:
            messages.success(request, "Email you entered is already in used")
        return HttpResponseRedirect(reverse('owner:profile'))
    


# Site Settings

def site(request):
    # Login Information Mangemenet

    login = LoginInterface.objects.all()
    
    if login:
        for i in login:
            login = i
            break
    if login:
        loginform = LoginInterfaceForm(instance=login)
    else:
        loginform = LoginInterfaceForm()


    # Sign Up information management


    signup = signupInterface.objects.all()    
    if signup:
        for i in signup:
            signup = i
            break
    print(signup)
    if signup:
        signform = signupInterfaceForm(instance=signup)
    else:
        signform = signupInterfaceForm()


    # Site Information and Manipulation

    site = SiteSetting.objects.all()    
    if site:
        for i in site:
            site = i
            break
    print(site)
    if site:
        form = SiteForm(instance=site)
    else:
        form = SiteForm()

    dist = {
        'form':form,
        'loginForm':loginform,
        'signForm': signform,
        'site':site,
        'login':login,
        'signup':signup
    }
    noti = notification(request)
    dist.update(noti)
    if request.method == 'POST':
        if site:
            form = SiteForm(request.POST, request.FILES, instance=site)
        else:
            form = SiteForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated Site Information")
            return HttpResponseRedirect(reverse('owner:site'))
        else:
            messages.error(request, "Something went Wrong")

    return render(request, 'owner/site.html', dist)

# Add Login Information
def addLoginData(request):

    login = LoginInterface.objects.all()
    
    if login:
        for i in login:
            login = i
            break
    
    if login:
        form = LoginInterfaceForm(request.POST, request.FILES, instance=i)
    else:
        form = LoginInterfaceForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        messages.success(request, "Successfully updated login information")
        
    else:
        messages.success(request, "Something went wrong")
    return HttpResponseRedirect(reverse('owner:site'))


def addSignData(request):

    login = signupInterface.objects.all()
    
    if login:
        for i in login:
            login = i
            break
    
    if login:
        form = signupInterfaceForm(request.POST, request.FILES, instance=login)
    else:
        form = signupInterfaceForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        messages.success(request, "Successfully updated Sign up information")
        
    else:
       
        messages.success(request, "Something went wrong")
    return HttpResponseRedirect(reverse('owner:site'))


def footerView(request):
    footer = Footor.objects.all().order_by('-id')
    form = FootorForm()
    dist = {
        'footer':footer,
        'form': form
    }
    noti = notification(request)
    dist.update(noti)
    if request.method == 'POST':
        form = FootorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added new footer")
            return HttpResponseRedirect(reverse('owner:footer'))
        else:
            dist.update({'form':form})
            messages.error(request,"something went wrong")

    return render(request, "owner/siteSetting/footor.html", dist)


def addNote(request, id):
    note = request.POST['note']
    trans = Transaction.objects.get(id = id)

    TransactionNote.objects.create(note = note, transaction = trans)
    messages.success(request, "Successfully added note")
    return HttpResponseRedirect(reverse('owner:transactionDetail', args=[id]))


def editNote(request, id):
    aa =  TransactionNote.objects.get(id=id)

    aa.note = request.POST['notes']
    aa.save()
    trans= aa.transaction.id
    messages.success(request, "Successfully updated note")
    return HttpResponseRedirect(reverse('owner:transactionDetail', args=[trans]))


def deleteNote(request, id):
  
    aa =  TransactionNote.objects.get(id=id)
    trans= aa.transaction.id
    aa.delete()
    messages.success(request, "Successfully deleted note")
    return HttpResponseRedirect(reverse('owner:transactionDetail', args=[trans]))



def SiteInformationView(request):

    # About Us
    about = AboutUs.objects.all()
    
    if about:
        for i in about:
            about = i
            break
    if about:
        aboutform = AboutForm(instance=about)
    else:
        aboutform = AboutForm()


    # Why Choose Us
    choose = ChooseUs.objects.all()
    
    if choose:
        for i in choose:
            choose = i
            break
    if choose:
        chooseform = ChooseForm(instance=choose)
    else:
        chooseform = ChooseForm()


    # Home Service
    homes = HomeService.objects.all()
    
    if homes:
        for i in homes:
            homes = i
            break
    if homes:
        homeform = HomeServiceForm(instance=homes)
    else:
        homeform = HomeServiceForm()

    dist = {
        'aboutform':aboutform,
        'about':about,
        'choose':choose,
        'chooseform':chooseform,
        'home':homes,
        'homeform':homeform
    }
    noti = notification(request)
    dist.update(noti)
    return render(request, "owner/siteSetting/siteInfo.html", dist)

# Add About Us Information
def aboutData(request):

    login = AboutUs.objects.all()
    
    if login:
        for i in login:
            login = i
            break
    
    if login:
        form = AboutForm(request.POST, request.FILES, instance=i)
    else:
        form = AboutForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        messages.success(request, "Successfully updated about us...")
        
    else:
        messages.success(request, "Something went wrong")
    return HttpResponseRedirect(reverse('owner:siteInfo'))


def chooseData(request):

    login = ChooseUs.objects.all()
    
    if login:
        for i in login:
            login = i
            break
    
    if login:
        form = ChooseForm(request.POST, request.FILES, instance=i)
    else:
        form = ChooseForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        messages.success(request, "Successfully updated why choose us...")
        
    else:
        messages.success(request, "Something went wrong")
    return HttpResponseRedirect(reverse('owner:siteInfo'))


def serviceData(request):

    login = HomeService.objects.all()
    
    if login:
        for i in login:
            login = i
            break
    
    if login:
        form = HomeServiceForm(request.POST, request.FILES, instance=i)
    else:
        form = HomeServiceForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        messages.success(request, "Successfully updated home service information...")
        
    else:
        messages.success(request, "Something went wrong")
    return HttpResponseRedirect(reverse('owner:siteInfo'))



def PolicyView(request):
    # Terms and Condiroon information management
    terms = Terms.objects.all()    
    if terms:
        for i in terms:
            terms = i
            break
    print(terms)
    if terms:
        terms_form = TermForm(instance=terms)
    else:
        terms_form = TermForm()


    # Site Information and Manipulation

    policy = Policy.objects.all()    
    if policy:
        for i in policy:
            policy = i
            break
    print(policy)
    if policy:
        policy_form = PolicyForm(instance=policy)
    else:
        policy_form = PolicyForm()

    dist = {
        'terms':terms,
        'policy':policy,
        'policy_form':policy_form,
        'terms_form':terms_form
    }
    noti = notification(request)
    dist.update(noti)
    return render(request, "owner/siteSetting/policy.html", dist)


def updateTerms(request):

    login = Terms.objects.all()
    
    if login:
        for i in login:
            login = i
            break
    
    if login:
        form = TermForm(request.POST, request.FILES, instance=login)
    else:
        form = TermForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        messages.success(request, "Successfully updated Terms and Conditions")
        
    else:
       
        messages.success(request, "Something went wrong")
    return HttpResponseRedirect(reverse('owner:policy'))


def updatePolicy(request):

    login = Policy.objects.all()
    
    if login:
        for i in login:
            login = i
            break
    
    if login:
        form = PolicyForm(request.POST, request.FILES, instance=login)
    else:
        form = PolicyForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        messages.success(request, "Successfully updated Policy and Privacy")
        
    else:
       
        messages.success(request, "Something went wrong")
    return HttpResponseRedirect(reverse('owner:policy'))

def SocialLinkView(request):
    social_link = SocialLink.objects.all().order_by('-id')
    form = SocialForm()
    dist = {
        'social':social_link,
        'form':form
    }
    noti = notification(request)
    dist.update(noti)
    if request.method == 'POST':
        form = SocialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Successfully Added Social Link")
        else:
            dist.update({'form':form})
            messages.error(request,"something went wrong")

    return render(request, "owner/siteSetting/socialLink.html", dist)


def SEOView(request):
    site = SEO.objects.all()    
    if site:
        for i in site:
            site = i
            break
    print(site)
    if site:
        form = SEOForm(instance=site)
    else:
        form = SEOForm()

    dist = {
        'form':form,
        'site':site,
    }
    noti = notification(request)
    dist.update(noti)
    if request.method == 'POST':
        if site:
            form = SEOForm(request.POST, request.FILES, instance=site)
        else:
            form = SEOForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated SEO Information")
            return HttpResponseRedirect(reverse('owner:seo'))
        else:
            messages.error(request, "Something went Wrong")


    return render(request, "owner/siteSetting/seo.html", dist)


def editFooter(request, id):
    footer = Footor.objects.get(id = id)
    footer.name = request.POST['footer_name']
    footer.link = request.POST['footer_link']
    footer.save()
    messages.success(request, "Successfully Edit Footer")
    return HttpResponseRedirect(reverse('owner:footer'))


def deleteFooter(request, id):
    footer = Footor.objects.get(id = id)
    footer.delete()
    messages.success(request, "Successfully deleted Footer")
    return HttpResponseRedirect(reverse('owner:footer'))


def editSocialLink(request, id):
    footer = SocialLink.objects.get(id = id)
    footer.name = request.POST['social_link_name']
    footer.icon = request.POST['social_icon']
    footer.link = request.POST['social_link']
    footer.save()
    messages.success(request, "Successfully Edited Social Link")
    return HttpResponseRedirect(reverse('owner:socialLink'))


def deleteSocialLink(request, id):
    footer = SocialLink.objects.get(id = id)
    footer.delete()
    messages.success(request, "Successfully deleted Social Link")
    return HttpResponseRedirect(reverse('owner:socialLink'))



# Site Information More and More
def brandView(request):
    return render(request, 'owner/siteSetting/brand.html')



# Country View
def countryView(request):
    country = Country.objects.all().order_by('-id')
    form = CountryForm()
    dist = {
        'country':country,
        'form': form
    }
    noti = notification(request)
    dist.update(noti)
    if request.method == 'POST':
        form = CountryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added new country")
            return HttpResponseRedirect(reverse('owner:country'))
        else:
            dist.update({'form':form})
            messages.error(request,"something went wrong")

    return render(request, "owner/country.html", dist)


def editCountry(request, id):
    footer = Country.objects.get(id = id)
    footer.name = request.POST['country_name']
    try:
        footer.flag_img = request.FILES['country_link']
    except:
        pass
    footer.save()
    messages.success(request, "Successfully Edited Country")
    return HttpResponseRedirect(reverse('owner:country'))


def deleteCountry(request, id):
    footer = Country.objects.get(id = id)
    footer.delete()
    messages.success(request, "Successfully deleted Country")
    return HttpResponseRedirect(reverse('owner:country'))


# Currency View
def currencyView(request):
    currency = Currency.objects.all().order_by('-id')
    form = CurrencyForm()
    dist = {
        'currency':currency,
        'form': form,
        'country':Country.objects.all()
    }
    noti = notification(request)
    dist.update(noti)
    if request.method == 'POST':
        form = CurrencyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added new currency")
            return HttpResponseRedirect(reverse('owner:currency'))
        else:
            dist.update({'form':form})
            messages.error(request,"something went wrong")

    return render(request, "owner/currency.html", dist)


def editCurrency(request, id):
    currency = Currency.objects.get(id = id)
    currency.country = Country.objects.get(id =request.POST['country']) 
    currency.currecy_rate = request.POST['currecy_rate']
    currency.conversion_rate = request.POST['conversion_rate']
    currency.commision_rate = request.POST['commision_rate']
    currency.currecy_sign = request.POST['currecy_sign']
    currency.save()
    messages.success(request, "Successfully Edited Currency")
    return HttpResponseRedirect(reverse('owner:currency'))



def deleteCurrency(request, id):
    footer = Currency.objects.get(id = id)
    footer.delete()
    messages.success(request, "Successfully deleted currency")
    return HttpResponseRedirect(reverse('owner:currency'))



# Country View
def pickupView(request):
    country = PickupPoint.objects.all().order_by('-id')
    form = PickupPointForm()
    dist = {
        'pickup':country,
        'form': form,
        'country':Country.objects.all()
    }
    noti = notification(request)
    dist.update(noti)
    if request.method == 'POST':
        form = PickupPointForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added new pickup point")
            return HttpResponseRedirect(reverse('owner:pickup'))
        else:
            dist.update({'form':form})
            messages.error(request,"something went wrong")

    return render(request, "owner/pickup.html", dist)


def editPickup(request, id):
    footer = PickupPoint.objects.get(id = id)
    footer.name = request.POST['name']
    footer.pickup_point  = request.POST['pickup_point']
    footer.country = Country.objects.get(id = request.POST['country'])
    footer.save()
    messages.success(request, "Successfully Edited Pickup Point")
    return HttpResponseRedirect(reverse('owner:pickup'))


def deletePickup(request, id):
    footer = PickupPoint.objects.get(id = id)
    footer.delete()
    messages.success(request, "Successfully deleted pickup point")
    return HttpResponseRedirect(reverse('owner:pickup'))


def kycView(request):
    kyc = KYC.objects.filter(customer__kyc_verified = False)
    

    dist = {
        'kyc':kyc.filter(customer__kyc_verified = True),
        'kyc_not':kyc.filter(customer__kyc_verified = False),
        'pending':kyc.filter(customer__kyc_verified = False).count(),
        'verified_ss':kyc.filter(customer__kyc_verified = True).count()
    }
    noti = notification(request)
    dist.update(noti)
    return render(request, "owner/kyc.html", dist)


def kycVerification(request, id):
    kyc = KYC.objects.get(id = id)
    # print(kyc)
    try:
        con = Country.objects.get(name = kyc.country)
    except:
        con = None
        
    dist  ={
        'kycs':kyc,
        'country':con
    }
   
    noti = notification(request)
    dist.update(noti)
    return render(request, "owner/kycDetail.html", dist)

def verifyView(request, id):
    user = Customer.objects.get(id = id)
    
    cm = KYC.objects.filter(customer = user)
  
    for i in cm:
        cm=i
        break


    sub = 'Your KYC is verified'
    messa = "We congraulate you for verifying your kyc. And you can add Bank, recipient and send money."
   
    other_info = siteInfo()
    
    recipient_list = [user.admin.email]
    dist_info = {
        'sub': sub, 'message':messa
    }
    dist_info.update(other_info)
    content = settings.EMAIL_HOST_USER
    html_message = render_to_string('component/email.html', dist_info)
    pain_html_msg = strip_tags(html_message)
    try: 
        msg = EmailMultiAlternatives(sub, pain_html_msg, content, recipient_list)
        msg.attach_alternative(html_message, "text/html")
        msg.send()
    except:
        messages.error(request,"KYC verified. However failed to sent email. Please ask to verify customer email")
    cust = user
    cust.kyc_verified = True
    cust.save()
    CustomerNotification.objects.create(customer = cust, name ="Congratulation Your KYC Has Been Verified.", types ="kyc", ids=cust.id)
    messages.success(request, "Successfully Verified Account")
    
    return HttpResponseRedirect(reverse('owner:kyc'))

def rejectView(request, id):
    user = Customer.objects.get(id = id)
    
    cm = KYC.objects.filter(customer = user)
  
    for i in cm:
        cm=i
        break

    cust = user
    cust.rejected = True
    cust.save()

    sub = 'Your KYC is rejected'
    messa = "We are sorry to inform you that your kyc is rejected, please update your details and try again."
    other_info = siteInfo()
    
    recipient_list = [user.admin.email]
    dist_info = {
        'sub': sub, 'message':messa
    }
    dist_info.update(other_info)
    content = settings.EMAIL_HOST_USER
    html_message = render_to_string('component/email.html', dist_info)
    pain_html_msg = strip_tags(html_message)
    try: 
        msg = EmailMultiAlternatives(sub, pain_html_msg, content, recipient_list)
        msg.attach_alternative(html_message, "text/html")
        msg.send()
    except:
        messages.error(request,"KYC rejected. However failed to sent email. Please ask to verify customer email")
    CustomerNotification.objects.create(customer = cust, name ="Sorry Your KYC Has Been Rejected.", types ="kyc", ids=cust.id)
    messages.success(request, "Successfully Rejected KYC")
    
    return HttpResponseRedirect(reverse('owner:kyc'))



# Sending Purpose and Source Fund Setting

def purposeView(request):
    purpose = SendingPurpose.objects.all().order_by('-id')
    form = PurposeForm()
    dist = {
        'purpose':purpose,
        'form': form
    }
    noti = notification(request)
    dist.update(noti)
    if request.method == 'POST':
        form = PurposeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added new sending purpose")
            return HttpResponseRedirect(reverse('owner:purpose'))
        else:
            dist.update({'form':form})
            messages.error(request,"something went wrong")

    return render(request, "owner/payment/sendingPurpose.html", dist)


def editPurpose(request, id):
    footer = SendingPurpose.objects.get(id = id)
    footer.name = request.POST['footer_name']

    footer.save()
    messages.success(request, "Successfully Edit Footer")
    return HttpResponseRedirect(reverse('owner:purpose'))


def deletePurpose(request, id):
    footer = SendingPurpose.objects.get(id = id)
    footer.delete()
    messages.success(request, "Successfully deleted Sending Purpose")
    return HttpResponseRedirect(reverse('owner:purpose'))



def fundView(request):
    footer = SourceFund.objects.all().order_by('-id')
    form = FundForm()
    dist = {
        'fund':footer,
        'form': form
    }
    noti = notification(request)
    dist.update(noti)
    if request.method == 'POST':
        form = FundForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added new source fund")
            return HttpResponseRedirect(reverse('owner:fund'))
        else:
            dist.update({'form':form})
            messages.error(request,"something went wrong")
    return render(request, "owner/payment/fund.html", dist)



def editFund(request, id):
    footer = SourceFund.objects.get(id = id)
    footer.name = request.POST['fund_name']
   
    footer.save()
    messages.success(request, "Successfully Edit Source Fund")
    return HttpResponseRedirect(reverse('owner:fund'))


def deleteFund(request, id):
    footer = SourceFund.objects.get(id = id)
    footer.delete()
    messages.success(request, "Successfully deleted Fund")
    return HttpResponseRedirect(reverse('owner:fund'))


def blockPlaceView(request):
    footer = BlockPlace.objects.all().order_by('-id')
    print(footer)
    form = BlockForm()
    dist = {
        'blocksw':footer,
        'form': form
    }
    noti = notification(request)
    dist.update(noti)
    if request.method == 'POST':
        form = BlockForm(request.POST)
        if form.is_valid():
            aa = form.save(commit=False)
            aa.block_status = True
            aa.save()
            messages.success(request, "Successfully Blocked " + str(aa.block) )
            return HttpResponseRedirect(reverse('owner:blockPlace'))
        else:
            dist.update({'form':form})
            messages.error(request, "something went wrong")
    return render(request, "owner/payment/restrict.html", dist)



def editBlockPlace(request, id):
    footer = BlockPlace.objects.get(id = id)
    footer.block_status = False
    footer.save()
    messages.success(request, "Successfully Allowed " + str(footer.block))
    return HttpResponseRedirect(reverse('owner:blockPlace'))


def deleteBlockPlace(request, id):
    footer = BlockPlace.objects.get(id = id)
    aa = str(footer.block)
    footer.delete()
    messages.success(request, "Successfully deleted " +  aa)
    return HttpResponseRedirect(reverse('owner:blockPlace'))

def editBlockPlaceBlock(request, id):
    footer = BlockPlace.objects.get(id = id)
    footer.block_status = True
    footer.save()
    messages.success(request, "Successfully Blocked " +  str(footer.block))
    return HttpResponseRedirect(reverse('owner:blockPlace'))
