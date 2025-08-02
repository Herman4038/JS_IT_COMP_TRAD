# backend/trading/views.py

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Inventory
from django.views.decorators.csrf import csrf_exempt
import json

# Custom login view
def login_view(request):
    if request.method == 'POST':  # Handle POST request (form submission)
        username = request.POST.get('username')  # Get the username from the form
        password = request.POST.get('password')  # Get the password from the form

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in and create a session
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after successful login
        else:
            # Return error if the credentials are invalid
            messages.error(request, 'Invalid username or password.')
            return render(request, 'index.html')

    return render(request, 'index.html')  # Render the login form on GET request


# Dashboard view with inventory management
@login_required
def dashboard(request):
    # Get session data for visit count
    visits = request.session.get('visit_count', 0)
    visits += 1
    request.session['visit_count'] = visits
    
    # Get search and filter parameters
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'item_name')
    sort_order = request.GET.get('order', 'asc')
    
    # Get all inventory items
    inventory_items = Inventory.objects.all()
    
    # Apply search filter
    if search_query:
        inventory_items = inventory_items.filter(
            Q(item_name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(serial_number__icontains=search_query)
        )
    
    # Apply sorting
    if sort_order == 'desc':
        sort_by = f'-{sort_by}'
    inventory_items = inventory_items.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(inventory_items, 12)  # Show 12 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate summary statistics
    total_items = inventory_items.count()
    total_value = sum(item.total_value for item in inventory_items)
    low_stock_items = inventory_items.filter(quantity__lte=5).count()
    out_of_stock_items = inventory_items.filter(quantity=0).count()
    
    context = {
        'visits': visits,
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_by': sort_by.replace('-', ''),
        'sort_order': sort_order,
        'total_items': total_items,
        'total_value': total_value,
        'low_stock_items': low_stock_items,
        'out_of_stock_items': out_of_stock_items,
    }
    
    return render(request, 'dashboard.html', context)


# Add new inventory item
@login_required
def add_inventory_item(request):
    if request.method == 'POST':
        try:
            data = request.POST
            inventory_item = Inventory.objects.create(
                item_name=data.get('item_name'),
                brand=data.get('brand'),
                model=data.get('model'),
                description=data.get('description'),
                unit_cost=float(data.get('unit_cost', 0)),
                srp_price=float(data.get('srp_price', 0)),
                quantity=int(data.get('quantity', 0)),
                serial_number=data.get('serial_number', ''),
            )
            
            # Handle image upload
            if 'item_picture' in request.FILES:
                inventory_item.item_picture = request.FILES['item_picture']
                inventory_item.save()
            
            messages.success(request, f'Item "{inventory_item.item_name}" added successfully!')
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f'Error adding item: {str(e)}')
            return redirect('dashboard')
    
    return render(request, 'add_inventory_item.html')


# Edit inventory item
@login_required
def edit_inventory_item(request, item_id):
    item = get_object_or_404(Inventory, id=item_id)
    
    if request.method == 'POST':
        try:
            data = request.POST
            item.item_name = data.get('item_name')
            item.brand = data.get('brand')
            item.model = data.get('model')
            item.description = data.get('description')
            item.unit_cost = float(data.get('unit_cost', 0))
            item.srp_price = float(data.get('srp_price', 0))
            item.quantity = int(data.get('quantity', 0))
            item.serial_number = data.get('serial_number', '')
            
            # Handle image upload
            if 'item_picture' in request.FILES:
                item.item_picture = request.FILES['item_picture']
            
            item.save()
            messages.success(request, f'Item "{item.item_name}" updated successfully!')
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f'Error updating item: {str(e)}')
    
    context = {'item': item}
    return render(request, 'edit_inventory_item.html', context)


# Delete inventory item
@login_required
def delete_inventory_item(request, item_id):
    item = get_object_or_404(Inventory, id=item_id)
    
    if request.method == 'POST':
        try:
            item_name = item.item_name
            item.delete()
            messages.success(request, f'Item "{item_name}" deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting item: {str(e)}')
    
    return redirect('dashboard')


# AJAX endpoint for quick item updates
@login_required
@csrf_exempt
def update_item_ajax(request, item_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item = get_object_or_404(Inventory, id=item_id)
            
            if 'quantity' in data:
                item.quantity = int(data['quantity'])
            if 'unit_cost' in data:
                item.unit_cost = float(data['unit_cost'])
            if 'srp_price' in data:
                item.srp_price = float(data['srp_price'])
            
            item.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Item updated successfully',
                'total_value': float(item.total_value),
                'stock_status': item.stock_status
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)
