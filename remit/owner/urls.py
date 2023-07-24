from django.urls import path
from .import views

app_name = "owner"

urlpatterns = [
    path('', views.Dashboard.as_view(), name ='dashboard'),
    path('super-profile', views.Profile.as_view(), name="profile"),

    # Customer Part
    path('customer-data', views.CustomerView.as_view(), name="customer"),
    path('customer-profile/<int:id>', views.customerProfile, name="customerProfile"),
    path('delete-customer/<int:id>', views.deleteCustomer, name = "deleteCustomer"),

    # Agent Part
    path('agent-data', views.AgentView, name = "agent"),
    path('agent-profile/<int:id>', views.agentProfile, name="agentProfile"),
    path('delete-agent/<int:id>', views.deleteAgent, name = "deleteAgent"),
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

    path('addabout', views.aboutData, name = "aboutdata"),
    path('addservice', views.serviceData, name = "serviceData"),
    path('chooseData', views.chooseData, name = "chooseData"),

    path('country-setting', views.countryView, name = "country"),
    path('editCountry/<int:id>', views.editCountry, name ="editCountry"),
    path('delete-Country/<int:id>', views.deleteCountry, name = "deleteCountry"),

    path('currency-setting', views.currencyView, name = "currency"),
    path('editCurrency/<int:id>', views.editCurrency, name ="editCurrency"),
    path('delete-Currency/<int:id>', views.deleteCurrency, name = "deleteCurrency"),

    path('pickup-setting', views.pickupView, name = "pickup"),
    path('editpickup/<int:id>', views.editPickup, name ="editPickup"),
    path('delete-pickup/<int:id>', views.deletePickup, name = "deletePickup"),


    # KYC Verification

    path(
        'kyc-verification-request-list/asda283sd', views.kycView, name="kyc"
    ),
    path(
        'verify-kyc-now/<int:id>', views.verifyView, name = "verify"
    ),
    path(
        'changeststus/<int:id>', views.changeStatus, name = "changeStatus"
    ),


    # Bank Information
    path(
        'owner-bank-information', views.bankView, name ="bank"
    ),
    path('filter-bank-account', views.filterBank, name ="filterBank"),

    # Email and SMS Settings
    path('email-setting', views.emailSetting, name = "emailSetting"),
    path('addEmailSetting/<int:id>', views.addEmailSetting, name = "addEmailSetting"),
    path('addSMSSetting/<int:id>', views.addSMSSetting, name = "addSMSSetting"),
    path('sms-setting', views.smsSetting, name = "smsSetting"),
    path('addDefaultNumber', views.addDefaultNumber, name = "addDefaultNumber"),
    path('banned-user-settings', views.bannedSetting, name = "bannedSetting"),
    path('banCustomer/<int:id>', views.banCustomer, name= "banCustomer"),
    path('banCustomerDisable/<int:id>', views.banCustomerDisable, name = "banCustomerDisable"),

    # Blog
    path(
        'blogs-news-event', views.blogView, name ="blog"
    ),
    path(
        'edit-blog/<int:id>', views.editBlog, name ="editblog"
    ),
    path('delete-blog/<int:id>', views.deleteBlog, name ="deleteBlog"),
    path('ticket-list', views.ticketList, name ="ticketView"),
    path('closeTicket/<int:id>', views.closeTicket, name ="closeTicket")

]   