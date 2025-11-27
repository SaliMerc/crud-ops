from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    
    brand=models.CharField(max_length=100, blank=True, null=True)
    category=models.CharField(max_length=100, blank=True, null=True)   
    quantity=models.IntegerField(default=1, blank=True, null=True) # set default as 1

    def __str__(self):
        return self.name
