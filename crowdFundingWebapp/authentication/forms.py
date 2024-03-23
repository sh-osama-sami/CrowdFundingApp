from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.utils import timezone


# registration form that inherits from UserCreationForm
class RegistrationForm(UserCreationForm): # registration form 
    email = forms.EmailField(max_length=254, help_text='Required. Please Enter a valid email address.')
    username = forms.CharField(max_length=30, help_text='Required. Please Enter a valid username.')
    mobile_phone = forms.CharField(max_length=11, help_text='Required. Please Enter a valid Egyptian phone number.')
    profile_picture = forms.ImageField(required=True) # request a profile pic from the user

    class Meta: # meta class
        model = CustomUser # model for the form
        fields = ('first_name', 'last_name', 'username', 'email', 'mobile_phone', 'password1', 'password2', 'profile_picture')  # Define the fields to be included in the form

    def clean_email(self):      # validation for email uniqueness
        email = self.cleaned_data.get('email')  # Get the email from the cleaned data
        if CustomUser.objects.filter(email=email).exists(): # Check if an existing user has the same email address
            raise ValidationError('This email address is already in use.') #if yes tell stop and tell the user 
        return email #else it is correct and new

    def clean_mobile_phone(self):     # validation for mobile phone format
        mobile_phone = self.cleaned_data.get('mobile_phone') # Get the mobile phone from the cleaned data
        valid_prefixes = ['011', '010', '012', '015']        # Validate against Egyptian phone number format
        if not any(mobile_phone.startswith(prefix) for prefix in valid_prefixes) or len(mobile_phone) != 11: # Check if the mobile phone number does not start with any valid prefix or its length is not 11
            raise ValidationError('Please enter a valid Egyptian phone number starting with 011, 010, 012, or 015.')   # Raise a validation error with a specific message
        return mobile_phone # Return the validated mobile phone number


class UserProfileForm(forms.ModelForm): # Define a form for user profile information
    class Meta:
        model = CustomUser  # Specify the model for the form
        fields = ['first_name', 'last_name', 'mobile_phone', 'profile_picture', 'birthdate', 'facebook_profile','country'] # Define the fields to be included in the form

    def clean_mobile_phone(self): # validation for mobile phone format
        mobile_phone = self.cleaned_data.get('mobile_phone') # Get the mobile phone from the cleaned data
        valid_prefixes = ['011', '010', '012', '015'] # Validate against Egyptian phone number format
        if not any(mobile_phone.startswith(prefix) for prefix in valid_prefixes) or len(mobile_phone) != 11:  # Check if the mobile phone number does not start with any valid prefix or its length is not 11
            raise ValidationError('Please enter a valid Egyptian phone number starting with 011, 010, 012, or 015.')  # Raise a validation error with a specific message
        return mobile_phone # Return the validated mobile phone number

    def clean_birthdate(self): # validation for birthdate
        birthdate = self.cleaned_data.get('birthdate')    # Get the birthdate from the cleaned data
        if birthdate and birthdate > timezone.now().date(): # Ensure birthdate is not in the future
            raise ValidationError('Please enter a valid birthdate.') # raise an erreor if the bd is in the future
        return birthdate # else return the BD




