from django.urls import path
from . import views

app_name = 'trading'

urlpatterns = [
    # path('', views.home, name='home'),     # if you have a home view
    path('dashboard/', views.dashboard, name='dashboard'),
]