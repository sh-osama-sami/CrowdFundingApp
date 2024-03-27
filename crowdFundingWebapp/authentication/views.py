from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import RegistrationForm
from django.db.models import Count
from Project.models import Project
from .forms import RegistrationForm, UserProfileForm
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import CustomUser


@login_required
def profile(request):
    return redirect('home')



def error_page(request):
    error_message = 'An error occurred.'
    return render(request, 'Project/error_page.html', {'error_message': error_message})


# render and handle registration form
def register(request):
    try:
        if request.method == 'POST':
            form = RegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                verification_email(request, user)
                messages.success(request, 'A verification email has been sent to your email address. Please verify your email.')
                return redirect('register')  # Redirect to the same page to display the message
        else:
            form = RegistrationForm()
    except ObjectDoesNotExist:
        return render(request, 'Project/error_page.html', {'error_message': 'An error occurred during registration.'})

    return render(request, 'registration/register.html', {'form': form})



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
        active_projects_count = Project.objects.filter(is_active=1).count()
        non_active_projects_count = Project.objects.filter(is_active=0).count()
        reported_projects = Project.objects.filter(is_reported=True).annotate(report_count=Count('reports'))
        return render(request, 'admin/admin_home.html', {'active_projects_count': active_projects_count, 'non_active_projects_count': non_active_projects_count, 'reported_projects': reported_projects})
    else:
        return redirect('administration')


@login_required
def view_profile(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)  # Retrieve the logged-in user object
    except ObjectDoesNotExist:
        # Handle the case where the user does not exist
        return render(request, 'profs/error.html', context={'error_message': 'User does not exist.'})
    return render(request, 'profs/view_profile.html', context={'user': user})

@login_required
def edit_profile(request, user_id):
    try:
        user = get_object_or_404(CustomUser, pk=user_id)
    except ObjectDoesNotExist:
        # Handle the case where the user does not exist
        return render(request, 'profs/error.html', context={'error_message': 'User does not exist.'})

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Handle the case where form saving failed
                return render(request, 'profs/error.html', context={'error_message': str(e)})
            return redirect('view_profile', user_id=user_id)
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'profs/edit_profile.html', context={'form': form})

@login_required
def delete_account(request, user_id):
    try:
        user = get_object_or_404(CustomUser, pk=user_id)
    except ObjectDoesNotExist:
        # Handle the case where the user does not exist
        return render(request, 'profs/error.html', context={'error_message': 'User does not exist.'})

    if request.method == 'POST':
        try:
            user.delete()
        except Exception as e:
            # Handle the case where user deletion failed
            return render(request, 'profs/error.html', context={'error_message': str(e)})
        return redirect('admin_home')  # Redirect to admin home after user deletion
    return render(request, 'profs/delete_account.html', context={'user_id': user_id})
