from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, EmailAuthenticationForm

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InstallationBookingForm
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from .models import CustomUser
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
# Create your views here.

def home(request):
    return render(request, 'pages/index.html')


# ------------------------------------
# A. Registration View
# ------------------------------------
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # works with username
            messages.success(request, "Registration successful!")
            return redirect("profile")
    else:
        form = CustomUserCreationForm()

    return render(request, "pages/register.html", {"form": form})

# ------------------------------------
# B. Custom Login View (The Authentication Fix)
# ------------------------------------

from django.contrib.auth.forms import AuthenticationForm

def custom_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profile")
    else:
        form = AuthenticationForm()

    return render(request, "pages/login.html", {"form": form})


# Logout View
def logout_view(request):
    logout(request)
    return redirect('login') # Redirecst the user back to the homepage



# Viewing the profile
# the user must be logged in to view their profile
@login_required
def profile_view(request):
    user = request.user
    installations = user.installations.all()  # Related name from model

    return render(request, "pages/profile.html", {
        "user": user,
        "installations": installations
    })


# Services Page you do not need to be logged in to view the services page
def services_view(request):
    return render(request, 'pages/services.html')

# You do not need to be logged in to view the company page
def company(request):
    return render(request , 'pages/company.html')


# Facts Page
def facts(request):
    return render(request, 'pages/facts.html')



@login_required
def installation(request):
    if request.method == "POST":
        form = InstallationBookingForm(request.POST)
        if form.is_valid():
            installation = form.save(commit=False)
            installation.user = request.user  # Assign logged-in user
            installation.save()

            messages.success(request, "Installation booked successfully!")
            return redirect("profile")  # Redirect to profile page after submission
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = InstallationBookingForm()

    return render(request, "pages/installation.html", {"form": form})

