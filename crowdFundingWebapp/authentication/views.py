from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import RegistrationForm
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def profile(request):
    # url = reverse('projects.index')
    # return redirect(url)
    return HttpResponse(" login successfulyy")


# render and handle registration form
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            verification_email(request, user)
            return HttpResponse('A verification email has been sent to your email address. Please verify your email.')

    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def verification_email(request, user):
    subject = 'Verify your email address for Crowd Funding'
    verification_link = request.build_absolute_uri('/authentication/verify/{}/'.format(user.id))
    message = 'Thank you for creating an account! Please verify your email address by clicking the link below:\n{}'.format(
        verification_link)
    from_email = 'sherry.osama.sami@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)


def verify_email(request, user_id):
    user = User.objects.get(pk=user_id)
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
        return redirect('admin_login')
