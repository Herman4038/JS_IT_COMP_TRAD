from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from backend.trading.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home: serve the login form
    path('', TemplateView.as_view(template_name='index.html'), name='home'),

    # Dashboard (after login)
    path('dashboard/', dashboard, name='dashboard'),

    # Override the login view to use index.html
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='index.html'),
        name='login'
    ),

    # Logout (you can leave this using the default template or redirect)
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(next_page='home'),
        name='logout'
    ),
]


# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 