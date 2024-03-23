from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import RegistrationForm, UserProfileForm
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import CustomUser


@login_required
def profile(request):
    user_id = request.user.id

    return redirect('view_profile', user_id=user_id)


def register(request):  # Define a view to render and handle the registration form
    if request.method == 'POST':  # Check if the request method is POST (form submission)
        form = RegistrationForm(request.POST, request.FILES)  # Create a form instance with POST data and files
        if form.is_valid():  # Check if the form data is valid
            user = form.save(commit=False)  # Save the form data without committing to the database yet
            user.is_active = False  # Set the user's active status to False initially
            user.save()  # Save the user object with the updated status
            verification_email(request, user)  # Send a verification email to the user
            messages.success(request,
                             'A verification email has been sent to your email address. Please verify your email.')
            return redirect('register')  # Redirect to the registration page to display a success message

    else:
        form = RegistrationForm()  # Create an empty registration form for GET requests
    return render(request, 'registration/register.html', {'form': form})  # Render the registration template with the form



# check if the user has activated his account before login
def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Your account is not activated. Please verify your email.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def verification_email(request, user):
    subject = 'Verify your email address for Crowd Funding'
    verification_link = request.build_absolute_uri('/authentication/verify/{}/'.format(user.id))
    message = 'Thank you for creating an account! Please verify your email address by clicking the link below:\n{}'.format(
        verification_link)
    from_email = 'sherry.osama.sami@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)


def verify_email(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    user.is_active = True
    user.save()
    messages.success(request, 'Your email has been verified. Please login.')
    return redirect('login')


def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin_home')
    else:
        form = AuthenticationForm()
    return render(request, 'admin/admin_login.html', {'form': form})


@login_required
def admin_home(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'admin/admin_home.html')
    else:
        return redirect('administration') #changed from admin_login beacuse it returns no such url or view


@login_required
def view_profile(request, user_id):
    user = CustomUser.objects.get(pk=user_id)  # Retrieve the logged-in user object
    return render(request, 'profs/view_profile.html', context={'user': user})


@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('view_profile', user_id=user_id)
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'profs/edit_profile.html', context={'form': form})


@login_required
def delete_account(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_home')  # Redirect to admin home after user deletion
    return render(request, 'profs/delete_account.html', context={'user_id': user_id})
