from django.shortcuts import render, get_object_or_404
from django.http import Http404
from language.models import Language
from .models import Course

def course_list(request, language):
    courses = Course.objects.filter(language__language=language).order_by('-id')
    return render(request, 'course/course.html', {'courses': courses})

def course_home(request):
    languages = Language.objects.all()
    return render(request, 'course/home.html', {'languages': languages})

def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, 'course/detail.html', {'course': course})
