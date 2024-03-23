from django.utils import timezone
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password


# registration form that inherits from UserCreationForm
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    username = forms.CharField(max_length=30, help_text='Required. Enter a valid username.')
    mobile_phone = forms.CharField(max_length=11, help_text='Required. Enter a valid Egyptian phone number.')
    profile_picture = forms.ImageField(required=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'mobile_phone', 'password1', 'password2',
                  'profile_picture')

    # validation for email uniqueness
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('This email address is already in use.')
        return email

    # validation for mobile phone format
    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data.get('mobile_phone')
        # Validate against Egyptian phone number format
        valid_prefixes = ['011', '010', '012', '015']
        if not any(mobile_phone.startswith(prefix) for prefix in valid_prefixes) or len(mobile_phone) != 11:
            raise ValidationError('Please enter a valid Egyptian phone number starting with 011, 010, 012, or 015.')
        return mobile_phone


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'mobile_phone', 'profile_picture', 'birthdate', 'facebook_profile',
                  'country']

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data.get('mobile_phone')
        # Validate against Egyptian phone number format
        valid_prefixes = ['011', '010', '012', '015']
        if not any(mobile_phone.startswith(prefix) for prefix in valid_prefixes) or len(mobile_phone) != 11:
            raise ValidationError('Please enter a valid Egyptian phone number starting with 011, 010, 012, or 015.')
        return mobile_phone

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        # Ensure birthdate is not in the future
        if birthdate and birthdate > timezone.now().date():
            raise ValidationError('Please enter a valid birthdate.')
        return birthdate