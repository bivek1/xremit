from django.urls import path
from .import views

app_name = "customer"

urlpatterns = [
    path('customer-dashboard', views.customerDashboard, name ="dashboard"),
    path('my-recipient', views.recipient, name ="recipient"),
    path('kyc-verification', views.kycVerify, name ="verify"),
    path('currency-now', views.currency, name = "currency"),
    path('send-money', views.sendMoney, name ="sendMoney"),

]   