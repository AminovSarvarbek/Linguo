from django.urls import path
from .views import login_view, activate, logout_view, profile_view, update_user

app_name = 'user'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('activate/', activate, name='activate'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', update_user, name='update'),
]
