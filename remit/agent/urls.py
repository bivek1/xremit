from django.urls import path
from .import views

app_name = "agent"

urlpatterns = [
    path('dashboard', views.dashboard, name="dashboard"),
    path('profile-agent', views.Profile.as_view(), name = "profile"),
    path('currency-setting', views.currencyView, name = "currency"),
    path('editCurrency/<int:id>', views.editCurrency, name ="editCurrency"),
    path('delete-Currency/<int:id>', views.deleteCurrency, name = "deleteCurrency"),
    path('customer-profile-pic', views.updatePic, name ="updatePic"),
]