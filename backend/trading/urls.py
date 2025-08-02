# js_it_comp_trad/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView  # Import Django's built-in LoginView
from backend.trading import views  # Import views from the backend/trading app

urlpatterns = [
    # Using Django's built-in LoginView to handle login
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # Login URL
    
    # Dashboard URL, protected by login_required
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard URL (requires login)
]
