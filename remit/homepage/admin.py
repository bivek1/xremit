from django.contrib import admin
from .models import Country, CustomUser, Customer, Agent, SocialLink, KYC, Recipient, Transaction, BankAccount, DefaultCurrency


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Customer)
admin.site.register(Agent)
admin.site.register(SocialLink)
admin.site.register(Country)
admin.site.register(KYC)
admin.site.register(Recipient)
admin.site.register(Transaction)
admin.site.register(BankAccount)
admin.site.register(DefaultCurrency)