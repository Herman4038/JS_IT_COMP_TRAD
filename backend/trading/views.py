from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Inventory, TimeLog, Sale, BuyItem
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import csv
import io
from decimal import Decimal
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['last_activity'] = timezone.now().isoformat()
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'index.html')

    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

@login_required
def dashboard(request):
    visits = request.session.get('visit_count', 0)
    visits += 1
    request.session['visit_count'] = visits
    
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'item_name')
    sort_order = request.GET.get('order', 'asc')
    
    inventory_items = Inventory.objects.all()
    
    if search_query:
        inventory_items = inventory_items.filter(
            Q(item_name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(serial_number__icontains=search_query)
        )
    
    if sort_order == 'desc':
        sort_by = f'-{sort_by}'
    inventory_items = inventory_items.order_by(sort_by)
    
    paginator = Paginator(inventory_items, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    total_items = inventory_items.count()
    total_value = sum(item.total_value for item in inventory_items)
    low_stock_items = inventory_items.filter(quantity__lte=5).count()
    out_of_stock_items = inventory_items.filter(quantity=0).count()
    
    current_time_log = TimeLog.objects.filter(user=request.user, is_active=True).first()
    
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
        'current_time_log': current_time_log,
        'session_timeout': settings.SESSION_TIMEOUT,
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def buy_item(request, item_id):
    item = get_object_or_404(Inventory, id=item_id)
    
    if request.method == 'POST':
        try:
            quantity_bought = int(request.POST.get('quantity', 1))
            supplier = request.POST.get('supplier', '')
            notes = request.POST.get('notes', '')
            
            if quantity_bought <= 0:
                messages.error(request, 'Quantity must be greater than 0.')
                return redirect('dashboard')
            
            unit_cost = float(request.POST.get('unit_cost', item.unit_cost))
            
            buy_item = BuyItem.objects.create(
                buyer=request.user,
                item=item,
                quantity_bought=quantity_bought,
                unit_cost=unit_cost,
                supplier=supplier,
                notes=notes
            )
            
            messages.success(request, f'Purchase recorded! {quantity_bought} units of {item.item_name} bought for ₱{buy_item.total_cost:,.2f}')
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f'Error recording purchase: {str(e)}')
    
    context = {
        'item': item,
        'session_timeout': settings.SESSION_TIMEOUT,
    }
    
    return render(request, 'buy_item.html', context)

@login_required
def buy_history(request):
    buy_items = BuyItem.objects.all().order_by('-purchase_date')
    
    date_filter = request.GET.get('date')
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            buy_items = buy_items.filter(purchase_date__date=filter_date)
        except ValueError:
            pass
    
    buyer_filter = request.GET.get('buyer')
    if buyer_filter:
        buy_items = buy_items.filter(buyer__username__icontains=buyer_filter)
    
    paginator = Paginator(buy_items, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    total_purchases = buy_items.count()
    total_cost = sum(buy_item.total_cost for buy_item in buy_items)
    
    context = {
        'page_obj': page_obj,
        'date_filter': date_filter,
        'buyer_filter': buyer_filter,
        'total_purchases': total_purchases,
        'total_cost': total_cost,
        'session_timeout': settings.SESSION_TIMEOUT,
    }
    
    return render(request, 'buy_history.html', context)

@login_required
def export_buy_history_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="js_it_buy_history_{timezone.localtime(timezone.now()).strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'Buyer', 'Item', 'Quantity Bought', 'Unit Cost', 'Total Cost', 'Supplier'])
    
    buy_items = BuyItem.objects.all().order_by('-purchase_date')
    
    for buy_item in buy_items:
        writer.writerow([
            buy_item.purchase_date.strftime('%Y-%m-%d %H:%M'),
            buy_item.buyer.username,
            buy_item.item.item_name,
            buy_item.quantity_bought,
            float(buy_item.unit_cost),
            float(buy_item.total_cost),
            buy_item.supplier
        ])
    
    return response

@login_required
def cashier(request):
    search_query = request.GET.get('search', '')
    inventory_items = Inventory.objects.filter(quantity__gt=0)
    
    if search_query:
        inventory_items = inventory_items.filter(
            Q(item_name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(inventory_items, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'session_timeout': settings.SESSION_TIMEOUT,
    }
    
    return render(request, 'cashier.html', context)

@login_required
def process_sale(request, item_id):
    item = get_object_or_404(Inventory, id=item_id)
    
    if request.method == 'POST':
        try:
            quantity_sold = int(request.POST.get('quantity', 1))
            customer_name = request.POST.get('customer_name', '')
            payment_method = request.POST.get('payment_method', 'Cash')
            notes = request.POST.get('notes', '')
            
            if quantity_sold <= 0:
                messages.error(request, 'Quantity must be greater than 0.')
                return redirect('cashier')
            
            if quantity_sold > item.quantity:
                messages.error(request, f'Not enough stock. Available: {item.quantity}')
                return redirect('cashier')
            
            unit_price = float(request.POST.get('unit_price', item.srp_price))
            
            sale = Sale.objects.create(
                cashier=request.user,
                item=item,
                quantity_sold=quantity_sold,
                unit_price=unit_price,
                customer_name=customer_name,
                payment_method=payment_method,
                notes=notes
            )
            
            messages.success(request, f'Sale processed successfully! {quantity_sold} units of {item.item_name} sold for ₱{sale.total_amount:,.2f}')
            return redirect('cashier')
            
        except Exception as e:
            messages.error(request, f'Error processing sale: {str(e)}')
    
    context = {
        'item': item,
        'session_timeout': settings.SESSION_TIMEOUT,
    }
    
    return render(request, 'process_sale.html', context)

@login_required
def sales_history(request):
    sales = Sale.objects.all().order_by('-sale_date')
    
    date_filter = request.GET.get('date')
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            sales = sales.filter(sale_date__date=filter_date)
        except ValueError:
            pass
    
    cashier_filter = request.GET.get('cashier')
    if cashier_filter:
        sales = sales.filter(cashier__username__icontains=cashier_filter)
    
    paginator = Paginator(sales, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    total_sales = sales.count()
    total_revenue = sum(sale.total_amount for sale in sales)
    
    context = {
        'page_obj': page_obj,
        'date_filter': date_filter,
        'cashier_filter': cashier_filter,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'session_timeout': settings.SESSION_TIMEOUT,
    }
    
    return render(request, 'sales_history.html', context)

@login_required
def export_sales_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="js_it_sales_{timezone.localtime(timezone.now()).strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'Cashier', 'Item', 'Quantity Sold', 'Unit Price', 'Total Amount', 'Customer', 'Payment Method'])
    
    sales = Sale.objects.all().order_by('-sale_date')
    
    for sale in sales:
        writer.writerow([
            sale.sale_date.strftime('%Y-%m-%d %H:%M'),
            sale.cashier.username,
            sale.item.item_name,
            sale.quantity_sold,
            float(sale.unit_price),
            float(sale.total_amount),
            sale.customer_name,
            sale.payment_method
        ])
    
    return response

@login_required
def time_in(request):
    active_session = TimeLog.objects.filter(user=request.user, is_active=True).first()
    
    if active_session:
        messages.warning(request, 'You already have an active time session.')
        return redirect('dashboard')
    
    TimeLog.objects.create(user=request.user, is_active=True)
    messages.success(request, f'Time in recorded at {timezone.localtime(timezone.now()).strftime("%I:%M %p")}')
    
    return redirect('dashboard')

@login_required
def time_out(request):
    active_session = TimeLog.objects.filter(user=request.user, is_active=True).first()
    
    if not active_session:
        messages.warning(request, 'No active time session found.')
        return redirect('dashboard')
    
    try:
        active_session.time_out = timezone.now()
        active_session.is_active = False
        active_session.save()
        
        duration = active_session.duration_hours
        messages.success(request, f'Time out recorded. Session duration: {duration} hours')
        
    except Exception as e:
        messages.error(request, f'Error recording time out: {str(e)}')
    
    return redirect('dashboard')

@login_required
def time_logs(request):
    time_logs = TimeLog.objects.all().order_by('-time_in')
    
    user_filter = request.GET.get('user')
    if user_filter:
        time_logs = time_logs.filter(user__username__icontains=user_filter)
    
    date_filter = request.GET.get('date')
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            time_logs = time_logs.filter(time_in__date=filter_date)
        except ValueError:
            pass
    
    paginator = Paginator(time_logs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    users = get_user_model().objects.filter(timelog__isnull=False).distinct()
    
    context = {
        'page_obj': page_obj,
        'users': users,
        'user_filter': user_filter,
        'date_filter': date_filter,
        'session_timeout': settings.SESSION_TIMEOUT,
    }
    
    return render(request, 'time_logs.html', context)

@login_required
def add_inventory_item(request):
    if request.method == 'POST':
        try:
            data = request.POST
            # Handle discount price - make it optional
            discount_price_data = data.get('discount_price', '')
            discount_price = float(discount_price_data) if discount_price_data and discount_price_data.strip() else None
            
            # Handle serial number - convert empty string to None
            serial_number_data = data.get('serial_number', '')
            serial_number = serial_number_data if serial_number_data.strip() else None
            
            inventory_item = Inventory.objects.create(
                item_name=data.get('item_name'),
                brand=data.get('brand'),
                model=data.get('model'),
                description=data.get('description'),
                unit_cost=float(data.get('unit_cost', 0)),
                srp_price=float(data.get('srp_price', 0)),
                discount_price=discount_price,
                quantity=int(data.get('quantity', 0)),
                serial_number=serial_number,
            )
            
            if 'item_picture' in request.FILES:
                inventory_item.item_picture = request.FILES['item_picture']
                inventory_item.save()
            
            messages.success(request, f'Item "{inventory_item.item_name}" added successfully!')
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f'Error adding item: {str(e)}')
            return redirect('dashboard')
    
    return render(request, 'add_inventory_item.html')

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
            
            # Handle discount price - make it optional
            discount_price_data = data.get('discount_price', '')
            item.discount_price = float(discount_price_data) if discount_price_data and discount_price_data.strip() else None
            
            item.quantity = int(data.get('quantity', 0))
            
            # Handle serial number - convert empty string to None
            serial_number_data = data.get('serial_number', '')
            item.serial_number = serial_number_data if serial_number_data.strip() else None
            
            if 'item_picture' in request.FILES:
                item.item_picture = request.FILES['item_picture']
            
            item.save()
            messages.success(request, f'Item "{item.item_name}" updated successfully!')
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f'Error updating item: {str(e)}')
    
    context = {'item': item}
    return render(request, 'edit_inventory_item.html', context)

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

@login_required
def export_inventory_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="js_it_inventory_{timezone.localtime(timezone.now()).strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    
    writer.writerow(['FOCUS', 'Model', 'Description', 'Quantity', 'SRP Price', 'DISCOUNT PRICE'])
    
    inventory_items = Inventory.objects.all().order_by('brand', 'item_name')
    
    for item in inventory_items:
        focus = item.brand if item.brand else 'Unknown'
        model = item.model if item.model else 'Unknown'
        description = item.description if item.description else item.item_name
        quantity = item.quantity
        srp_price = float(item.srp_price)
        discount_price = float(item.discount_price) if item.discount_price else 0.0
        
        writer.writerow([focus, model, description, quantity, srp_price, discount_price])
    
    return response

@login_required
def import_inventory_csv(request):
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            messages.error(request, 'Please select a CSV file to import.')
            return redirect('dashboard')
        
        csv_file = request.FILES['csv_file']
        
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a valid CSV file.')
            return redirect('dashboard')
        
        try:
            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.reader(io.StringIO(decoded_file))
            
            next(csv_data, None)
            
            imported_count = 0
            updated_count = 0
            errors = []
            
            for row_num, row in enumerate(csv_data, start=2):
                try:
                    if len(row) >= 6:
                        focus, model, description, quantity, srp_price, discount_price = row[:6]
                        
                        focus = focus.strip() if focus else 'Unknown'
                        model = model.strip() if model else 'Unknown'
                        description = description.strip() if description else ''
                        quantity = int(quantity) if quantity.isdigit() else 0
                        srp_price = float(srp_price) if srp_price.replace('.', '').replace(',', '').isdigit() else 0.0
                        discount_price = float(discount_price) if discount_price.replace('.', '').replace(',', '').isdigit() else 0.0
                        
                        existing_item = Inventory.objects.filter(
                            brand__iexact=focus,
                            model__iexact=model
                        ).first()
                        
                        if existing_item:
                            existing_item.description = description
                            existing_item.quantity = quantity
                            existing_item.srp_price = srp_price
                            existing_item.discount_price = discount_price
                            existing_item.save()
                            updated_count += 1
                        else:
                            Inventory.objects.create(
                                item_name=f"{focus} {model}",
                                brand=focus,
                                model=model,
                                description=description,
                                quantity=quantity,
                                srp_price=srp_price,
                                discount_price=discount_price
                            )
                            imported_count += 1
                    else:
                        errors.append(f"Row {row_num}: Insufficient columns")
                        
                except Exception as e:
                    errors.append(f"Row {row_num}: {str(e)}")
            
            if imported_count > 0 or updated_count > 0:
                success_msg = f"Import completed: {imported_count} new items imported, {updated_count} items updated."
                if errors:
                    success_msg += f" {len(errors)} errors occurred."
                messages.success(request, success_msg)
            
            if errors:
                for error in errors[:5]:
                    messages.warning(request, error)
                if len(errors) > 5:
                    messages.warning(request, f"... and {len(errors) - 5} more errors")
            
        except Exception as e:
            messages.error(request, f'Error processing CSV file: {str(e)}')
    
    return redirect('dashboard')

@login_required
def csv_import_view(request):
    return render(request, 'csv_import.html')
