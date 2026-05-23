from django.db import models

from cloudinary.models import CloudinaryField

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    stock = models.IntegerField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    thumbnail = CloudinaryField('image')

    def __str__(self):
        return self.title




