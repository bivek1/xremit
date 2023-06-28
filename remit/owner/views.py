
from django.shortcuts import render
from django.views.generic import View, UpdateView
from homepage.models import Feature, Service, Client, Testomonial, Footor, Brand, AboutUs, ChooseUs, HomeService
from homepage.models import CompanyInformation, CustomUser
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from homepage.models import Blog, Customer, Agent, Owner, LoginInterface, signupInterface, Policy, Terms, SocialLink


from .models import SiteSetting, SEO
from .forms import SiteForm, SEOForm, FeatureForm, AboutForm, HomeServiceForm, ChooseForm
from homepage.forms import CustomerForm

from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from homepage.forms import UserCreateForm, UserUpdateForm, ServiceForm, ClientForm, TestomonialForm, CompanyInformationForm, BlogForm, CategoryForm, SubCategoryForm

from .forms import LoginInterfaceForm, signupInterfaceForm, AboutForm, SEOForm, BrandForm, FootorForm, SocialForm, PolicyForm, TermForm

# Create your views here.




class Dashboard(View):
    template_name = "owner/dashboard.html"
    def get(self, request, *args, **kwargs, ):
        blog = Blog.objects.all()[:4]

        dist = {
            'blog':blog,
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
        
        return render(request, self.template_name, dist)
    

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
                obj.zip_code = request.POST['zip_code']
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
    real_customer = Customer.objects.get(id = id)


    form = CustomerForm(instance=real_customer)
    dist = {
        'real_customer':real_customer,
        'form':form,
        'form_head':"Update Customer",
        'button':"Update customer",
    
    }

    if request.method == 'POST':
        try: 
            real_customer.admin.first_name = request.POST['first_name']
            real_customer.admin.last_name = request.POST['last_name']
            real_customer.admin.email = request.POST['email']
            real_customer.admin.username = request.POST['email']
            real_customer.admin.save()
        except:
            messages.error(request, "Email is added already..")
            return HttpResponseRedirect(reverse('owner:customerProfile',args=[real_customer.id]))
        form = CustomerForm(request.POST, instance=real_customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated Customer")
            return HttpResponseRedirect(reverse('owner:customerProfile',args=[real_customer.id]))
        else:
            messages.error(request, "Something went wrong")
    return render(request, 'owner/customerProfile.html',dist)

# Add Customer
# class CustomerView(CreateView):
#     model = Customer
    
#     template_name = 
#     custom_user = None

#     def post(self, request):
#         form = CustomerForm(request.POST)
#         # try:
#         custom_user = CustomUser.objects.create_user(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], username = request.POST['email'], password = request.POST['password'], user_type = 'customer')
#         if form.is_valid():
#             form.save(commit = False)
#             form.admin = custom_user
#             form.added_by = request.user
#             form.save()
#             messages.success(request, "Successfully Added Customer")
#         except:
#             messages.error(request, "Email already exist")
#             # return render(request, self.template_name, self.get_context_data)
       
#         return HttpResponseRedirect(reverse('owner:customer'))

 
    
   
    

# Add Agent
class AgentView(CreateView):
    pass




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
     

        return render(request, self.template_name, dist)
    def post(self, request, *args, **kwargs):
        form = FeatureForm(request.POST)
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
       

        return render(request, self.template_name, dist)
    def post(self, request, *args, **kwargs):
        form = ClientForm(request.POST)
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


        return render(request, self.template_name, dist)
    def post(self, request, *args, **kwargs):
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added Blog")
            return HttpResponseRedirect(reverse('staff:addBlog'))
        else:
            messages.success(request, "Something went Wrong")
            return HttpResponseRedirect(reverse('staff:addBlog'))


class UpdateBlog(SuccessMessageMixin,UpdateView):
    template_name = "staff/editBlog.html"
    model = Blog
    form_class = BlogForm
    success_message = "Successfully Updated Blog"
    
    def get_success_url(self, *args, **kwargs):
        id = self.kwargs['pk']
        return reverse('staff:updateBlog', args=[id])
def deleteBlog(request, id):
    blog = Blog.objects.get(id = id)
    blog.delete()
    messages.success(request, "Succesfully Deleted Blog")
    return HttpResponseRedirect(reverse('staff:addBlog')) 




# Profle Crud>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class Profile(UpdateView, SuccessMessageMixin):
    template_name = "staff/other/profile.html"
    model = CustomUser
    form_class = UserUpdateForm
    success_message = "Successfully Updated Profile"
    
    def get_success_url(self, *args, **kwargs):
        id = self.kwargs['pk']
        return reverse('owner:updateAdmin', args=[id])
    


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

