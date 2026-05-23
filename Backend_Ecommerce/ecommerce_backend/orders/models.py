from django.db import models

from django.contrib.auth.models import User

from products.models import Product

from datetime import datetime

import random

# Create your models here.

class Order(models.Model):

    PAYMENT_CHOICES=[
        ("cash_on_delivery", "Cash on Delivery"),
        ("upi", "UPI"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]

    ORDER_STATUS_CHOICES = [
        ("placed", "Placed"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")

    order_code = models.CharField(max_length=30, unique=True, blank=True)

    name=models.CharField(max_length=100)

    phone=models.CharField(max_length=10)

    address=models.TextField()

    city=models.CharField(max_length=100)

    state=models.CharField(max_length=100)

    pincode = models.CharField(max_length=6)

    payment =models.CharField(max_length=30,choices=PAYMENT_CHOICES)

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending"
    )

    order_status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default="placed"
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    shipping_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        if not self.order_code:
            date_part = datetime.now().strftime("%Y%m%d")
            random_part = random.randint(1000, 9999)
            self.order_code = f"ORD-{date_part}-{random_part}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"



class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product.title} - {self.quantity}"



