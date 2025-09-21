from django.urls import path
from .views import ai_service_view

urlpatterns = [
    path("ai/", ai_service_view, name="ai_service"),
]
