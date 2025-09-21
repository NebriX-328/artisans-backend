from django.shortcuts import render

def index(request):
    return render(request, "marketplace/index.html")

def marketplace(request):
    return render(request, "marketplace/marketplace.html")

def awards(request):  
    return render(request, "marketplace/awards.html")

def competitions(request):  
    return render(request, "marketplace/competitions.html")

def explore(request):   
    return render(request, "marketplace/explore.html")

def login(request):   
    return render(request, "marketplace/login.html")

def profile1(request):   
    return render(request, "marketplace/profile1.html")

def payment(request):   
    return render(request, "marketplace/payment.html")

def artist(request):   
    return render(request, "marketplace/artist.html")