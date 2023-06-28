from django.shortcuts import render

# Create your views here.
def customerDashboard(request):
    return render(request, "customer/dashboard.html")

def recipient(request):
    return render(request, "customer/recipient.html")

def sendMoney(request):
    return render(request, "customer/sendMoney.html")

def currency(request):
    return render(request, "customer/currency.html")

def kycVerify(request):
    return render(request, "customer/verify.html")