from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import RegistrationForm
from django.http import HttpResponse


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
