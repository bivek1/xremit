from django.urls import path
from .import views

app_name = "owner"

urlpatterns = [
    path('', views.Dashboard.as_view(), name ='dashboard'),
    path('customer-data', views.CustomerView.as_view(), name="customer"),
    path('agent-data', views.AgentView.as_view(), name = "agent")
]