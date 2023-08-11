from django.contrib import admin
from .models import SiteSetting, SEO
from homepage.models import AboutUs, Brand ,LoginInterface, signupInterface, Policy, Footor, Service, Client, Testomonial, Terms, SocialLink, TopHeader, CompanyInformation
# Register your models here.
admin.site.register(LoginInterface)
admin.site.register(signupInterface)
admin.site.register(SiteSetting)