from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("marketplace/", views.marketplace, name="marketplace"),  
    path("awards/", views.awards, name="awards"),  
    path("competitions/", views.competitions, name="competitions"),  
    path("explore/", views.explore, name="explore"), 
    path("login/", views.login, name="login"),  
    path("profile1/", views.profile1, name="profile1"),  
    path("payment/", views.payment, name="payment"), 
    path("artist/", views.artist, name="artist"), 
] 



