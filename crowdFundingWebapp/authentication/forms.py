from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password


# registration form that inherits from UserCreationForm
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    username = forms.CharField(max_length=30, help_text='Required. Enter a valid username.')
    mobile_phone = forms.CharField(max_length=11, help_text='Required. Enter a valid Egyptian phone number.')
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'mobile_phone', 'password1', 'password2', 'profile_picture')

    # validation for email uniqueness
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email address is already in use.')
        return email

    # validation for mobile phone format
    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data.get('mobile_phone')
        if not mobile_phone.startswith('01') or len(mobile_phone) != 11:
            raise ValidationError('Enter a valid Egyptian phone number.')
        return mobile_phone

