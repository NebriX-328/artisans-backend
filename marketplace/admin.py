from django.contrib import admin
from .models import Artisan, Artwork

@admin.register(Artisan)
class ArtisanAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio')  # use actual fields from Artisan model

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'artisan')  # use actual fields from Artwork model
