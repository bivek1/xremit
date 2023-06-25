from django.urls import path
from .import views

app_name = "owner"

urlpatterns = [
    path('', views.Dashboard.as_view(), name ='dashboard'),

    # Customer Part
    path('customer-data', views.CustomerView.as_view(), name="customer"),
    path('customer-profile/<int:id>', views.customerProfile, name="customerProfile"),
    path('delete-customer/<int:id>', views.deleteCustomer, name = "deleteCustomer"),

    # Agent Part
    path('agent-data', views.AgentView.as_view(), name = "agent"),

    #Site Settings
    path('site-setting', views.site, name="site"),
    path('AddLoginData', views.addLoginData, name = "addLoginData"),
    path('AddSignupData', views.addSignData, name = "addSignData"),
    path('footer-setting', views.footerView, name = "footer"),
    path('terms-and-policy-setting', views.PolicyView, name = "policy"),
    path('site-extra-information', views.SiteInformationView, name = "siteInfo"),
    path('social-link-setting', views.SocialLinkView, name = "socialLink"),
    path('seo-optimization', views.SEOView, name = "seo"),

    # Edit and Delete site setting
    path('editFooter/<int:id>', views.editFooter, name ="editFooter"),
    path('delete-footer/<int:id>', views.deleteFooter, name = "deleteFooter"),
    path('editSocialLink/<int:id>', views.editSocialLink, name ="editSocialLink"),
    path('delete-socialLink/<int:id>', views.deleteSocialLink, name = "deleteSocialLink"),
    path('updateTerms', views.updateTerms, name ="updateTerms"),
    path('updatePolicy', views.updatePolicy, name ="updatePolicy"),

    # Futher Site Settings

    path('owner-brand', views.AddBrand.as_view(), name="addBrand"),
    path('<int:id>/deletebrand', views.deleteBrand, name="deleteBrand"),
    path('<pk>/updatebrand', views.UpdateBrand.as_view(), name="updateBrand"),

    path('owner-features', views.AddFeature.as_view(), name="addFeature"),
    path('<int:id>/deletefeatures', views.deleteFeature, name="deleteFeature"),
    path('<pk>/updatefeatures', views.UpdateFeature.as_view(), name="updateFeature"),
    # Url For Client------->
    # --------------------->
    path('owner-client', views.AddClient.as_view(), name="addClient"),
    path('<int:id>/deleteClient', views.deleteClient, name="deleteClient"),
    path('<pk>/updateClient', views.UpdateClient.as_view(), name="updateClient"),

    # Url For Testomonial------->
    # --------------------->
    path('owner-testomonial', views.AddTestomonial.as_view(), name="addTestomonial"),
    path('<int:id>/deleteTestomonial', views.deleteTestomonial, name="deleteTestomonial"),
    path('<pk>/updateTestomonial', views.UpdateTestomonial.as_view(), name="updateTestomonial"),
    # Url For Service------->
    # --------------------->
    path('owner-Service', views.AddService.as_view(), name="addService"),
    path('<int:id>/deleteService', views.deleteService, name="deleteService"),
    path('<pk>/updateService', views.UpdateService.as_view(), name="updateService"),
]   