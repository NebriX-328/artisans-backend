from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ai/", include("ai_service")),
    path("", include("marketplace.urls")),  # ✅ this loads marketplace urls
]

