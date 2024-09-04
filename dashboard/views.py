from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from language.models import Language
from user.models import CustomUser

@login_required
def dashboard_view(request):
    languages = Language.objects.all()
    return render(request, 'dashboard/home.html', {'languages': languages})

@login_required
def users_view(request):
    users = CustomUser.objects.all().order_by('-id')
    return render(request, 'dashboard/users.html', {'users': users})
