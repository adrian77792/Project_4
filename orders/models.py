from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone
 
class Order(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'
    STATUS_CANCELLED = 'cancelled'
    STATUS_FULFILLED = 'fulfilled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Oczekujące'),
        (STATUS_PAID, 'Zapłacone'),
        (STATUS_FULFILLED, 'Zrealizowane'),
        (STATUS_CANCELLED, 'Anulowane'),
    ]
 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stripe_payment_intent = models.CharField(max_length=255, null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    shipping_address = models.JSONField(null=True, blank=True)  # jeśli DB nie wspiera JSONField -> TextField
    note = models.TextField(blank=True)
 
    def calculate_total(self):
        total = Decimal('0.00')
        for item in self.items.all():
            total += item.line_total()
        return total
 
    def set_paid(self, stripe_payment_intent=None):
        self.status = self.STATUS_PAID
        self.paid_at = timezone.now()
        if stripe_payment_intent:

            self.stripe_payment_intent = stripe_payment_intent
        self.save()
 
    def __str__(self):
        return f"Order #{self.pk} - {self.status}"
 
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT)
    variant = models.ForeignKey('products.ProductVariant', null=True, blank=True, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
 
    def line_total(self):
        return self.unit_price * self.quantity
 
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
