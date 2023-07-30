from django.urls import path
from .import views

app_name = "homepage"
handler404 = views.handler404
urlpatterns = [
    path('', views.Homepage, name = 'homepage'),
    path('login', views.LoginV, name = 'login'),
    path('sign-up', views.Register, name = 'register'),
    path('logout', views.LogoutV, name = 'logout'),
    path('check-password', views.checkPassword, name = "checkPassword"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('services', views.serviceView, name = "services"),
    path('contact-us-xremit', views.contactView, name = "contact"),
    path('serviceDetails/<int:id>/<str:name>', views.serviceDetail, name = "serviceDetail"),
    path('about-xremit', views.aboutView, name = "about"),
    path('blog-news-and-event', views.blogView, name = "blog"),
    path('blogDetails/<int:id>/<str:name>', views.blogDetail, name = "blogDetail"),
    path('coutries', views.countryView, name = "country"),
    path('currency', views.currencyView, name = "currency"),
    path('feature', views.featureView, name = "feature"),
    path('featureDetails/<int:id>/<str:name>', views.featureDetail, name = "featureDetail"),
    path('sitemap', views.sitemapView, name = "sitemap"),
    path('privacy-and-policy-xremit', views.privacyView, name = "privacy"),
    path('terms-and-condition', views.termsView, name = "terms"),
    path('set_session_small', views.set_session_small, name = "set_session_small"),
    path('set_session_big', views.set_session_big, name = "set_session_big"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('OTP-VERFIFICATION-CODE-SENT-AUTOMATICALLY', views.OPTV, name ='OTPV'),
]