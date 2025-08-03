from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from backend.trading.views import (
    dashboard, 
    login_view, 
    logout_view,
    add_inventory_item, 
    edit_inventory_item, 
    delete_inventory_item,
    update_item_ajax,
    export_inventory_csv,
    import_inventory_csv,
    csv_import_view,
    time_in,
    time_out,
    time_logs,
    cashier,
    process_sale,
    sales_history,
    export_sales_csv,
    buy_item,
    buy_history,
    export_buy_history_csv
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', TemplateView.as_view(template_name='index.html'), name='home'),

    path('dashboard/', dashboard, name='dashboard'),

    path('time/in/', time_in, name='time_in'),
    path('time/out/', time_out, name='time_out'),
    path('time/logs/', time_logs, name='time_logs'),

    path('inventory/add/', add_inventory_item, name='add_inventory_item'),
    path('inventory/edit/<int:item_id>/', edit_inventory_item, name='edit_inventory_item'),
    path('inventory/delete/<int:item_id>/', delete_inventory_item, name='delete_inventory_item'),
    path('inventory/update/<int:item_id>/ajax/', update_item_ajax, name='update_item_ajax'),

    path('inventory/export/csv/', export_inventory_csv, name='export_inventory_csv'),
    path('inventory/import/csv/', import_inventory_csv, name='import_inventory_csv'),
    path('inventory/import/', csv_import_view, name='csv_import_view'),

    path('buy/item/<int:item_id>/', buy_item, name='buy_item'),
    path('buy/history/', buy_history, name='buy_history'),
    path('buy/history/export/csv/', export_buy_history_csv, name='export_buy_history_csv'),

    path('cashier/', cashier, name='cashier'),
    path('cashier/sale/<int:item_id>/', process_sale, name='process_sale'),
    path('cashier/sales/', sales_history, name='sales_history'),
    path('cashier/sales/export/csv/', export_sales_csv, name='export_sales_csv'),

    path('accounts/login/', login_view, name='login'),

    path('accounts/logout/', logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
