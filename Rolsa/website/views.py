from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, EmailAuthenticationForm

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InstallationBookingForm
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
# Create your views here.

def home(request):
    return render(request, 'pages/index.html')


# ------------------------------------
# A. Registration View
# ------------------------------------
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('') # Adjust 'home' to your main landing page name
    else:
        form = CustomUserCreationForm()
    
    # Ensure you have a template at 'pages/register.html'
    return render(request, 'pages/register.html', {'form': form})

# ------------------------------------
# B. Custom Login View (The Authentication Fix)
# ------------------------------------
def custom_login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            # Pass email as 'username' argument for the EmailBackend
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('')
            else:
                messages.error(request, 'Invalid email or password.')
                return render(request, 'pages/login.html', {'form': form})
    else:
        form = EmailAuthenticationForm()
    
    # Ensure you have a template at 'registration/login.html'
    return render(request, 'pages/login.html', {'form': form})
##


# Logout View
def logout_view(request):
    logout(request)
    return redirect('') # Redirecst the user back to the homepage



# Viewing the profile
# the user must be logged in to view their profile
@login_required
def profile_view(request):
    return render(request, 'pages/profile.html')


# Services Page you do not need to be logged in to view the services page
def services_view(request):
    return render(request, 'pages/services.html')

# You do not need to be logged in to view the company page
def company(request):
    return render(request , 'pages/company.html')


# Facts Page
def facts(request):
    return render(request, 'pages/facts.html')


def installation(request):
    if request.method == "POST":
        form = InstallationBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # link to logged-in user
            booking.save()
            messages.success(request, "Your installation booking has been submitted and saved to your profile!")
            return redirect("profile")  # redirect to profile page
    else:
        form = InstallationBookingForm()

    return render(request, "pages/installation.html", {"form": form})