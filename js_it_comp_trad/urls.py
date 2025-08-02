# urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from backend.trading.views import (
    dashboard, 
    login_view, 
    add_inventory_item, 
    edit_inventory_item, 
    delete_inventory_item,
    update_item_ajax
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home: serve the login form
    path('', TemplateView.as_view(template_name='index.html'), name='home'),

    # Dashboard (after login)
    path('dashboard/', dashboard, name='dashboard'),

    # Inventory Management
    path('inventory/add/', add_inventory_item, name='add_inventory_item'),
    path('inventory/edit/<int:item_id>/', edit_inventory_item, name='edit_inventory_item'),
    path('inventory/delete/<int:item_id>/', delete_inventory_item, name='delete_inventory_item'),
    path('inventory/update/<int:item_id>/ajax/', update_item_ajax, name='update_item_ajax'),

    # Use custom login view
    path('accounts/login/', login_view, name='login'),

    # Logout (you can leave this using the default template or redirect)
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(next_page='home'),
        name='logout'
    ),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
