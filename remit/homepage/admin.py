from django.contrib import admin
from .models import CustomUser, Customer, Agent, SocialLink


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Customer)
admin.site.register(Agent)
admin.site.register(SocialLink)