from django.db import models
from django.contrib.auth.models import User
from products.models import Item
from decimal import Decimal
from .utils import generate_unique_order_id  # we'll create this


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    unique_id = models.CharField(max_length=12, unique=True, editable=False)  # NEW
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Assign unique_id only on creation
        if not self.unique_id:
            self.unique_id = generate_unique_order_id()
        super().save(*args, **kwargs)

    def calculate_total(self):
        """Calculate total based on related OrderItems"""
        total = Decimal("0.00")
        for item in self.order_items.all():
            total += item.price * item.quantity
        self.total_amount = total
        return total

    def __str__(self):
        return f"Order {self.unique_id} by {self.customer.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item.name} (x{self.quantity})"

