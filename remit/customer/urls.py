from django.urls import path
from .import views

app_name = "customer"

urlpatterns = [
    path('customer-dashboard', views.customerDashboard, name ="dashboard"),
    path('my-deleteRecipient/<int:id>', views.deleteRecipient, name ="deleteRecipient"),
    path('editRecipient/<int:id>', views.editRecipient, name ="editRecipient"),
    path('my-recipient', views.recipient, name ="recipient"),
    path('add-recipient', views.addRecipient, name ="addRecipient"),
    path('kyc-verification', views.kycVerify, name ="verify"),
    path('currency-now', views.currency, name = "currency"),
    path('send-money', views.sendMoney, name ="sendMoney"),
    path('profile-customer', views.Profile.as_view(), name = "profile"),

]   