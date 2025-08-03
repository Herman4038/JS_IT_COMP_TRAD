from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils import timezone

class TimeLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Employee")
    time_in = models.DateTimeField(auto_now_add=True, verbose_name="Time In")
    time_out = models.DateTimeField(null=True, blank=True, verbose_name="Time Out")
    is_active = models.BooleanField(default=True, verbose_name="Active Session")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Time Log"
        verbose_name_plural = "Time Logs"
        ordering = ['-time_in']
    
    def __str__(self):
        return f"{self.user.username} - {self.time_in.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def duration(self):
        if self.time_out:
            time_in = timezone.localtime(self.time_in) if timezone.is_aware(self.time_in) else timezone.make_aware(self.time_in)
            time_out = timezone.localtime(self.time_out) if timezone.is_aware(self.time_out) else timezone.make_aware(self.time_out)
            return time_out - time_in
        return None
    
    @property
    def duration_hours(self):
        if self.duration:
            return round(self.duration.total_seconds() / 3600, 2)
        return 0

class BuyItem(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Buyer")
    item = models.ForeignKey('Inventory', on_delete=models.CASCADE, verbose_name="Item Purchased")
    quantity_bought = models.PositiveIntegerField(verbose_name="Quantity Bought")
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Cost")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Cost")
    supplier = models.CharField(max_length=100, blank=True, verbose_name="Supplier")
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="Purchase Date")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Buy Item"
        verbose_name_plural = "Buy Items"
        ordering = ['-purchase_date']
    
    def __str__(self):
        return f"{self.item.item_name} - {self.quantity_bought} units - {self.purchase_date.strftime('%Y-%m-%d %H:%M')}"
    
    def save(self, *args, **kwargs):
        if not self.total_cost:
            self.total_cost = self.quantity_bought * self.unit_cost
        super().save(*args, **kwargs)
        
        self.item.quantity += self.quantity_bought
        self.item.save()

class Sale(models.Model):
    cashier = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Cashier")
    item = models.ForeignKey('Inventory', on_delete=models.CASCADE, verbose_name="Item Sold")
    quantity_sold = models.PositiveIntegerField(verbose_name="Quantity Sold")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Price")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Amount")
    sale_date = models.DateTimeField(auto_now_add=True, verbose_name="Sale Date")
    customer_name = models.CharField(max_length=100, blank=True, verbose_name="Customer Name")
    payment_method = models.CharField(max_length=50, default="Cash", verbose_name="Payment Method")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Sale"
        verbose_name_plural = "Sales"
        ordering = ['-sale_date']
    
    def __str__(self):
        return f"{self.item.item_name} - {self.quantity_sold} units - {self.sale_date.strftime('%Y-%m-%d %H:%M')}"
    
    def save(self, *args, **kwargs):
        if not self.total_amount:
            self.total_amount = self.quantity_sold * self.unit_price
        super().save(*args, **kwargs)
        
        if self.item.quantity >= self.quantity_sold:
            self.item.quantity -= self.quantity_sold
            self.item.save()

class Inventory(models.Model):
    item_name = models.CharField(max_length=200, verbose_name="Item Name")
    brand = models.CharField(max_length=100, verbose_name="Brand", default="Unknown")
    model = models.CharField(max_length=100, verbose_name="Model", default="Unknown")
    description = models.TextField(verbose_name="Item Description", blank=True, default="")
    
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
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Discount Price",
        null=True,
        blank=True,
        help_text="Discounted selling price (optional)"
    )
    
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
    
    item_picture = models.ImageField(
        upload_to='inventory_images/', 
        blank=True, 
        null=True,
        verbose_name="Item Picture"
    )
    
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    
    class Meta:
        verbose_name = "Inventory Item"
        verbose_name_plural = "Inventory Items"
        ordering = ['item_name']
    
    def clean(self):
        """Convert empty serial numbers to None to avoid unique constraint violations"""
        if self.serial_number == '':
            self.serial_number = None
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.brand} {self.model} - {self.item_name}"
    
    @property
    def total_value(self):
        return self.unit_cost * self.quantity
    
    @property
    def profit_margin(self):
        if self.unit_cost > 0:
            return ((self.srp_price - self.unit_cost) / self.unit_cost) * 100
        return 0
    
    @property
    def stock_status(self):
        if self.quantity == 0:
            return "Out of Stock"
        elif self.quantity <= 5:
            return "Low Stock"
        else:
            return "In Stock"