from django.dispatch import receiver
from allauth.socialaccount.signals import pre_social_login, social_account_added
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

@receiver(pre_social_login)
def handle_pre_social_login(sender, request, sociallogin, **kwargs):
    User = get_user_model()
    email = sociallogin.account.extra_data.get('email')
    if email and not User.objects.filter(email=email).exists():
        raise PermissionDenied("User with this email does not exist.")

@receiver(social_account_added)
def handle_social_account_added(sender, request, sociallogin, **kwargs):
    User = get_user_model()
    email = sociallogin.account.extra_data.get('email')
    if email and not User.objects.filter(email=email).exists():
        raise PermissionDenied("User with this email does not exist.")
