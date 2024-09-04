from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.http import Http404
from .models import CustomUser
from .forms import UserUpdateForm, UserLoginForm


def login_view(request):
    """
    Handles user login. Sends a confirmation email if the user exists.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get("email")
        try:
            # Check if the user already exists
            user = CustomUser.objects.get(email=email.lower())
            user.send_confirmation_email()
            return redirect(f'{reverse("user:activate")}?email={email}')
        except CustomUser.DoesNotExist:
            # If user does not exist, create and send confirmation email
            form = UserLoginForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.send_confirmation_email()
                return redirect(f'{reverse("user:activate")}?email={user.email}')            
    else:
        form = UserLoginForm()

    return render(request, 'user/login.html', {'form': form})


def activate(request):
    """
    Handles user activation via OTP sent to their email.
    """
    email = request.GET.get("email")
    
    # Retrieve the user by email
    try:
        user = CustomUser.objects.get(email=email.lower())
    except CustomUser.DoesNotExist:
        raise Http404("User does not exist")

    if request.method == 'POST':
        # Combine OTP input fields
        otp = ''.join([request.POST.get(f'otp{i}', '') for i in range(1, 6)])
        
        # Check if the entered OTP matches
        if str(user.confirmation_code) == otp:
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard:home')
        else:
            # If OTP is incorrect, return error message
            return render(request, 'user/profile/activate.html', {
                'error_message': 'Incorrect OTP. Please try again.'
            })
    
    return render(request, 'user/profile/activate.html')


@login_required
def logout_view(request):
    """
    Logs out the user and redirects to the home page.
    """
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    """
    Displays the user's profile page.
    """
    return render(request, 'user/profile/profile.html')


@login_required
def update_user(request):
    """
    Handles updating the user's profile information.
    """
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('user:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)

    return render(request, 'user/profile/update.html', {'form': user_form})
