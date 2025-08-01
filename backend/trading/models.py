from django.db import models

class Inventory(models.Model):
    item_name = models.CharField(max_length=100)
    quantity  = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.item_name} ({self.quantity})"