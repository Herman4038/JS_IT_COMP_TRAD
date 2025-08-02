from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Inventory(models.Model):
    # Basic Information
    item_name = models.CharField(max_length=200, verbose_name="Item Name")
    brand = models.CharField(max_length=100, verbose_name="Brand", default="Unknown")
    model = models.CharField(max_length=100, verbose_name="Model", default="Unknown")
    description = models.TextField(verbose_name="Item Description", blank=True, default="")
    
    # Pricing Information
    unit_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Unit Cost",
        default=Decimal('0.01')
    )
    srp_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="SRP Price",
        default=Decimal('0.01')
    )
    
    # Inventory Information
    quantity = models.PositiveIntegerField(
        default=0, 
        validators=[MinValueValidator(0)],
        verbose_name="Quantity"
    )
    serial_number = models.CharField(
        max_length=100, 
        unique=True, 
        blank=True, 
        null=True,
        verbose_name="Serial Number"
    )
    
    # Image
    item_picture = models.ImageField(
        upload_to='inventory_images/', 
        blank=True, 
        null=True,
        verbose_name="Item Picture"
    )
    
    # Metadata
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    
    class Meta:
        verbose_name = "Inventory Item"
        verbose_name_plural = "Inventory Items"
        ordering = ['item_name']
    
    def __str__(self):
        return f"{self.brand} {self.model} - {self.item_name}"
    
    @property
    def total_value(self):
        """Calculate total inventory value"""
        return self.unit_cost * self.quantity
    
    @property
    def profit_margin(self):
        """Calculate profit margin percentage"""
        if self.unit_cost > 0:
            return ((self.srp_price - self.unit_cost) / self.unit_cost) * 100
        return 0
    
    @property
    def stock_status(self):
        """Get stock status"""
        if self.quantity == 0:
            return "Out of Stock"
        elif self.quantity <= 5:
            return "Low Stock"
        else:
            return "In Stock"