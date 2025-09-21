from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('ai_api/', include('ai_api.urls')),
    path("", include("marketplace.urls")),  # ✅ this loads marketplace urls
]
