from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from Admin.roles import AdminRole, DriverRole, UserRole
from rolepermissions.roles import assign_role

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        extra_fields.setdefault('role', 'admin') 

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('driver', 'Driver'),
        ('user', 'User'),
    ]

    username = models.CharField(max_length=150, blank=True, null=True, unique=False)

    email = models.EmailField(max_length=191, unique=True) 
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True) 

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='user')  

    objects = CustomUserManager()  

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.assign_role_permissions()

    def assign_role_permissions(self):
        role_mapping = {
            'admin': AdminRole,
            'driver': DriverRole,
            'user': UserRole,
        }

        role_class = role_mapping.get(self.role.lower())  
        if role_class:
            assign_role(self, role_class)
        else:
            assign_role(self, UserRole)

    def __str__(self):
        return self.email or self.username or "No Email"

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    
    brand=models.CharField(max_length=100, blank=True, null=True)
    category=models.CharField(max_length=100, blank=True, null=True)   
    quantity=models.IntegerField(default=0, blank=True, null=True)
    
    image=models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """To store payment transactions made by users for products.
    In real-world applications, the transactions table would be linked to a User model and Products model to know who made a payment to which product. This can be achieved using ForeignKey relationships.
    Having the transaction method makes your table flexible to accommodate different payment methods.
    Transaction status helps to track the state of the payment. After a payment is initiated, it should never be pending, but only either completed or failed.
    """
    
    CHOICES_TRANSACTION_STATUS = [
        ('pending', 'Pending'),
        ('failed', 'Failed'),
        ('completed', 'Completed'),
    ]
    
    CHOICES_TRANSACTION_METHOD = [
        ('mpesa', 'M-PESA'),
        ('credit_or_debit_card', 'Credit/Debit Card'),
    ]
    
    customer_name = models.CharField(max_length=100)
    customer_phone_number= models.CharField(max_length=15)
    
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_method= models.CharField(max_length=30, choices=CHOICES_TRANSACTION_METHOD, default='mpesa')
    
    transaction_status= models.CharField(max_length=20, choices=CHOICES_TRANSACTION_STATUS, default='pending')
    transaction_code = models.CharField(max_length=100, blank=True, null=True)
    transaction_reference_number = models.CharField(max_length=100, unique=True)
    transaction_result_description = models.TextField(blank=True, null=True)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.transaction_code} - {self.transaction_status}"