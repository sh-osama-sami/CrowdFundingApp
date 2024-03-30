from django.utils import timezone
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation


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
        if not any(mobile_phone.startswith(prefix) for prefix in valid_prefixes):
            raise ValidationError('Please enter a valid Egyptian phone number starting with 011, 010, 012, or 015')
        if len(mobile_phone) != 11:
            raise ValidationError('Please enter 11 digits!')
        return mobile_phone




class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        # You can add additional validation if needed

        return cleaned_data


class UserProfileForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'mobile_phone', 'profile_picture', 'birthdate', 'facebook_profile', 'country']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }

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

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password or confirm_password:
            if password != confirm_password:
                raise ValidationError('Passwords do not match.')

            try:
                password_validation.validate_password(password)
            except ValidationError as error:
                self.add_error('password', error)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user