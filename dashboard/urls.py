from django.urls import path
from .views import dashboard_view, users_view

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard_view, name='home'),
    path('users/', users_view, name='users'),
]
