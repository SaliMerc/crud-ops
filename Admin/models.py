from django.db import models

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
    transaction_code = models.CharField(max_length=100, unique=True)
    transaction_reference_number = models.CharField(max_length=100, unique=True)
    transaction_result_description = models.TextField(blank=True, null=True)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.transaction_code} - {self.transaction_status}"