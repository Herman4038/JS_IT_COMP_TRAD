from django.contrib import admin
from django.utils.html import format_html
from .models import Inventory, TimeLog

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = [
        'item_picture_display', 
        'item_name', 
        'brand', 
        'model', 
        'quantity', 
        'unit_cost', 
        'srp_price', 
        'total_value_display', 
        'stock_status_display',
        'date_added'
    ]
    list_filter = [
        'brand', 
        'date_added', 
        'last_updated'
    ]
    search_fields = [
        'item_name', 
        'brand', 
        'model', 
        'description', 
        'serial_number'
    ]
    list_editable = ['quantity', 'unit_cost', 'srp_price']
    readonly_fields = [
        'date_added', 
        'last_updated', 
        'total_value', 
        'profit_margin', 
        'stock_status'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('item_name', 'brand', 'model', 'description')
        }),
        ('Pricing', {
            'fields': ('unit_cost', 'srp_price')
        }),
        ('Inventory', {
            'fields': ('quantity', 'serial_number')
        }),
        ('Image', {
            'fields': ('item_picture',)
        }),
        ('Calculated Fields', {
            'fields': ('total_value', 'profit_margin', 'stock_status'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('date_added', 'last_updated'),
            'classes': ('collapse',)
        }),
    )
    
    def item_picture_display(self, obj):
        if obj.item_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />',
                obj.item_picture.url
            )
        return format_html(
            '<div style="width: 50px; height: 50px; background-color: #f8f9fa; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: #6c757d; font-size: 12px;">No Image</div>'
        )
    item_picture_display.short_description = 'Image'
    
    def total_value_display(self, obj):
        return f"₱{obj.total_value:,.2f}"
    total_value_display.short_description = 'Total Value'
    
    def stock_status_display(self, obj):
        status_colors = {
            'In Stock': 'success',
            'Low Stock': 'warning',
            'Out of Stock': 'danger'
        }
        color = status_colors.get(obj.stock_status, 'secondary')
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color, obj.stock_status
        )
    stock_status_display.short_description = 'Stock Status'
    
    class Media:
        css = {
            'all': ('admin/css/inventory_admin.css',)
        } 

@admin.register(TimeLog)
class TimeLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'time_in', 'time_out', 'duration_hours', 'is_active', 'get_date']
    list_filter = ['is_active', 'time_in', 'user']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'notes']
    readonly_fields = ['time_in', 'duration_hours']
    date_hierarchy = 'time_in'
    
    def get_date(self, obj):
        return obj.time_in.date()
    get_date.short_description = 'Date'
    
    fieldsets = (
        ('Employee Information', {
            'fields': ('user',)
        }),
        ('Time Tracking', {
            'fields': ('time_in', 'time_out', 'is_active')
        }),
        ('Session Details', {
            'fields': ('duration_hours', 'notes'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return False 