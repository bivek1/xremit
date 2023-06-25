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

]   