from django.db import models

class Artisan(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name


class Artwork(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='artworks/', blank=True, null=True)
    artisan = models.ForeignKey(Artisan, on_delete=models.CASCADE, related_name="artworks")

    def __str__(self):
        return self.title
