from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
from django.core.mail import send_mail


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
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')  # Redirection to the login page after successful registration
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
