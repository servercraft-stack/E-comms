from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
CAT_CHOICES = [
    ('electronics', 'Electronics'),
    ('fashion', 'Fashion'),
    ('home', 'Home & Garden'),
    ('books', 'Books'),
    ('toys', 'Toys & Games'),
    ('sports', 'Sports & Outdoors'),
    ('beauty', 'Beauty & Personal Care'),
    ('automotive', 'Automotive'),
    ('health', 'Health & Wellness'),
    ('grocery', 'Grocery & Gourmet Food'),
]



class Products(models.Model):
    name = models.CharField(max_length=255)
    desccription = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    category = models.CharField(max_length=255, choices=CAT_CHOICES, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.SET_NULL, null=True, blank=True)
    delivery_service = models.ForeignKey('DeliveryService', on_delete=models.SET_NULL, null=True, blank=True)

    delivery_address = models.TextField(blank=True, null=True)
    delivery_postal_code = models.CharField(max_length=20, blank=True, null=True)
    delivery_city = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return f"Order #{self.id} by {self.user.email}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.products.name} in Order #{self.order.id}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"Cart of {self.user.first_name} {self.user.last_name}"
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.products.price * self.quantity

PAYMENT_CHOICES = [
    ('credit_card', 'Credit Card'),
    ('debit_card', 'Debit Card'),
    ('paypal', 'PayPal'),
]
    



class PaymentMethod(models.Model):
    name = models.CharField(max_length=100, choices=PAYMENT_CHOICES)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return dict(PAYMENT_CHOICES).get(self.name, self.name)

class DeliveryService(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_delivery_time = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name






