from django.urls import path
from .import views

app_name = "homepage"

urlpatterns = [
    path('', views.Homepage, name = 'homepage'),
    path('login', views.LoginV, name = 'login'),
    path('sign-up', views.Register, name = 'register'),
    path('logout', views.LogoutV, name = 'logout'),
    path('check-password', views.checkPassword, name = "checkPassword"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('services', views.serviceView, name = "services")
]