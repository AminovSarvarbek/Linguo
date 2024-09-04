import random
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomUserManager

# Custom validator for confirmation_code
def validate_min_length(value):
    if value < 1000:
        raise ValidationError('Confirmation code must be at least 4 digits.')

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    confirmation_code = models.PositiveIntegerField(validators=[validate_min_length], blank=True, null=True) 
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        # Convert email to lowercase before saving
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)

    def generate_confirmation_code(self):
        self.confirmation_code = random.randint(10000, 99999)
        self.save()

    def send_confirmation_email(self):
        if not self.confirmation_code:
            self.generate_confirmation_code()

        subject = 'Linguo Confirmation'
        message = f'Your confirmation code: {self.confirmation_code}.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.email]

        send_mail(subject, message, from_email, recipient_list)

