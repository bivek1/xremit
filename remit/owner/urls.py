from django.urls import path
from .import views

app_name = "owner"

urlpatterns = [
    path('', views.Dashboard.as_view(), name ='dashboard'),
    # Customer Part
    path('customer-data', views.CustomerView.as_view(), name="customer"),
    path('customer-profile/<int:id>', views.customerProfile, name="customerProfile"),
    path('delete-customer', views.deleteCustomer, name = "deleteCustomer"),

    # Agent Part
    path('agent-data', views.AgentView.as_view(), name = "agent")
]