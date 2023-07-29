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
    path('changeCurone', views.changeCurone, name ="changeCurone"),
    path('complete-transaction', views.completePayment, name ="completePayment"),
    path('customer-transaction', views.transactionView, name ="transaction"),
    path('customer-bank-account', views.bankView, name ="bank"),
    path('customer-default-currency', views.defaultCurrencyView, name ="defaultCurrency"),
    path('two-factor-authentication', views.TwoFactorView, name ="twoFactor"),
    path('two-factor-authentication-google', views.GoogleOtpView, name ="gmailOtp"),
    path('two-factor-authentication-sms', views.phoneOtpView, name ="phoneOtp"),
    path('two-factor-authentication-phoneOtp', views.disablesms, name ="disablesms"),
    path('two-factor-authentication-disablegmail', views.disablegmail, name ="disablegmail"),
    path('customer-profile-pic', views.updatePic, name ="updatePic"),
    path('customer-find-bank', views.findBank, name ="findBank"),
    path('customer-get-bank', views.getBank, name ="getBank"),
    path('editBank/<int:id>', views.editBank, name ="editBank"),
    path('deleteBank/<int:id>', views.deleteBank, name ="deleteBank"),
    path('create-a-ticket-support-xremit', views.ticketView, name ="ticketView"),
    path('customer-ticket-list', views.ticketList, name ="ticketList"),
    path('csutomer-seen-notification', views.seenNotification, name="seenNotification"),
    path('customer-all-notification', views.allNotification, name="allNotification"),
    path('search-customer-data/', views.search, name='search'),
]   