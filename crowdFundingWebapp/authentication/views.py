from datetime import timedelta

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import RegistrationForm, CustomAuthenticationForm
from django.db.models import Count
from django.utils import timezone

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
                messages.success(request,
                                 'A verification email has been sent to your email address. Please verify your email.', extra_tags=["login", "success"])
                return redirect('login')  # Redirect to the same page to display the message
        else:
            form = RegistrationForm()
    except ObjectDoesNotExist:
        return render(request, 'Project/error_page.html', {'error_message': 'An error occurred during registration.'})

    return render(request, 'registration/register.html', {'form': form})


#
# def signin(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         print(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('home')
#                 else:
#                     messages.error(request, 'Your account is not activated. Please verify your email.')
#             else:
#                 # Authentication failed (invalid username or password)
#                 messages.error(request, 'Invalid username or password.')
#         else:
#             # Form is invalid
#             messages.error(request, 'You either have not verified your email or entered invalid credentials.')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'registration/login.html', {'form': form})

# def signin(request):
#     try:
#         if request.method == 'POST':
#             form = AuthenticationForm(data=request.POST)
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 if user.is_superuser==0:
#
#                     if user.is_active:
#                         login(request, user)
#                         return redirect('home')
#                     else:
#                         messages.error(request, 'Your account is not activated. Please verify your email.',extra_tags=["login","error"])
#                 else:
#                     messages.error(request, 'admin cannot login here',extra_tags=["login","error"])
#             else:
#                 print(user)
#                 messages.info(request, 'Invalid username or password.',extra_tags=["login","error"])
#         else:
#             form = AuthenticationForm()
#     except ObjectDoesNotExist:
#         return render(request, 'Project/error_page.html', {'error_message': 'An error occurred during login.'})
#     return render(request, 'registration/login.html', {'form': form})


def signin(request):
    try:
        if request.method == 'POST':
            form = CustomAuthenticationForm(data=request.POST)

            if form.is_valid():
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')

                try:
                    user = CustomUser.objects.get(email=email)
                except CustomUser.DoesNotExist:
                    messages.info(request, 'Invalid Email.', extra_tags=["login", "error"])
                    return render(request, 'registration/login.html', {'form': form})

                user = authenticate(request, username=user.username, password=password)

                if user is not None:
                    if not user.is_superuser:
                        if user.is_active:
                            login(request, user)
                            return redirect('home')
                        else:
                            messages.error(request, 'Your account is not activated. Please verify your email.', extra_tags=["login", "error"])
                    else:
                        messages.error(request, 'admin cannot login here', extra_tags=["login", "error"])
                else:
                    messages.info(request, 'Invalid password.', extra_tags=["login", "error"])
        else:
            form = CustomAuthenticationForm()
    except ObjectDoesNotExist:
        return render(request, 'Project/error_page.html', {'error_message': 'An error occurred during login.'})
    return render(request, 'registration/login.html', {'form': form,'email':request.GET.get('email' )})

def resend_verification_email(request, email):
    try:
        user = User.objects.get(email=email)
        print(user)
        verification_email(request, user)
        messages.success(request, 'A verification email has been sent to your email address. Please verify your email.',extra_tags=["login","success"])
    except ObjectDoesNotExist:
        messages.error(request, 'User does not exist.',extra_tags=["login","error"])
    return redirect('login')  # Redirect to the same page to display the message

def verification_email(request, user):
    try:
        subject = 'Verify your email address for Crowd Funding'
        verification_token = generate_verification_token(user.id)
        verification_link = request.build_absolute_uri('/authentication/verify/{}/{}'.format(user.id, verification_token))
        message = 'Thank you for creating an account! Please verify your email address by clicking the link below:\n{}'.format(
            verification_link)
        from_email = 'sherry.osama.sami@gmail.com'
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        return render(request, 'Project/error_page.html', {'error_message': str(e)})


def generate_verification_token(user_id):
    # Generate a token based on user_id and current timestamp
    timestamp = timezone.now() + timedelta(minutes=1)  # Token expires after 24 hours
    token = '{}_{}'.format(user_id, timestamp.timestamp())
    return token


def verify_email(request, user_id, token):
    try:
        user = CustomUser.objects.get(pk=user_id)
        if check_verification_token(user_id, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your email has been verified. Please login.',extra_tags=["login","success"])
        else:
            messages.error(request, 'expired verification link.',extra_tags=["login", "error", "verify"])
        return redirect(reverse('login') + f'?email={user.email}')
    except ObjectDoesNotExist:
        return render(request, 'Project/error_page.html',
                      {'error_message': 'An error occurred during email verification.'})


def check_verification_token(user_id, token):
    try:
        user_id_from_token, timestamp = token.split('_')
        user_id_from_token = int(user_id_from_token)
        timestamp = float(timestamp)
        # Check if the token is valid (user_id matches and not expired)
        if user_id == user_id_from_token and timezone.now().timestamp() < timestamp:
            return True
    except (ValueError, AttributeError):
        pass
    return False


def admin_login(request):
    try:
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
                    form.add_error(None, "Invalid username or password")
        else:
            form = AuthenticationForm()
    except Exception as e:
            return render(request, 'admin/admin_errors.html', {'error_message': str(e)})
    return render(request, 'admin/admin_login.html', {'form': form})


@login_required
def admin_home(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            all_projects = Project.objects.all()
            active_projects_count = 0
            suspended_projects_count = 0
            completed_projects_count = 0
            for project in all_projects:
                status = project.get_status()
                if status == "Active":
                    active_projects_count += 1
                elif status == "Suspended":
                    suspended_projects_count += 1
                elif status == "Reached Target":
                    completed_projects_count += 1

            reported_projects = Project.objects.filter(is_reported=True).annotate(report_count=Count('reports'))
            return render(request, 'admin/admin_home.html', {'active_projects_count': active_projects_count,
                                                            'suspended_projects_count': suspended_projects_count,
                                                            'completed_projects_count': completed_projects_count,
                                                            'reported_projects': reported_projects})
        else:
            return redirect('administration')
    except Exception as e:
            return render(request, 'admin/admin_errors.html', {'error_message': str(e)})



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
