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
            form.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')  # Redirection to the login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

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
    

