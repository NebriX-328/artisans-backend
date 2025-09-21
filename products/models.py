from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    craft_type = models.CharField(max_length=255)   # <-- Must exist
    artisan_name = models.CharField(max_length=255, default="Unknown Artisan")
    price = models.FloatField()
    
    def __str__(self):
        return self.name
