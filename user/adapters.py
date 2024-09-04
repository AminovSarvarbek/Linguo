from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()

# Custom adapter for handling additional user actions during account creation
class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        # Log activity for debugging purposes
        print("Custom Account adapter")

        # Save the user using the default method without committing to DB
        user = super().save_user(request, user, form, commit=False)

        # Convert email to lowercase before saving
        user.email = user.email.lower()

        # Custom behavior: Automatically activate the user
        user.is_active = True

        # Only save the user to DB if commit is True
        if commit:
            user.save()

        return user


# Custom adapter for handling social login-specific behavior
class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Log activity for debugging purposes
        print("Custom Social Account adapter")

        # Convert social login email to lowercase before processing
        email = sociallogin.account.extra_data.get('email')
        if email:
            sociallogin.account.extra_data['email'] = email.lower()

        # Check if the user already exists in the system
        if sociallogin.is_existing:
            user = sociallogin.user
            # Ensure the existing user is active
            if not user.is_active:
                user.is_active = True
                user.save()

        else:
            # Check if a user with the same email exists
            if email:
                try:
                    # Fetch the existing user by email
                    existing_user = User.objects.get(email=email.lower())
                    # Attach the existing user to the social login process
                    sociallogin.user = existing_user
                    sociallogin.state['process'] = 'connect'
                except User.DoesNotExist:
                    # If no user exists, activate the new social user account
                    sociallogin.user.is_active = True
                    sociallogin.user.save()