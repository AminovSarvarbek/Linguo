from django.urls import path
from .views import course_list, course_home, course_detail

app_name = 'course'

urlpatterns = [
    path('', course_home, name='home'),
    path('detail/<int:id>/', course_detail, name='detail'),
    path('courses/<str:language>/', course_list, name='courses'),
]
