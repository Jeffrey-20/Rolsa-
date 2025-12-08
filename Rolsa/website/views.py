from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, EmailAuthenticationForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InstallationBookingForm
# Create your views here.

def home(request):
    return render(request, 'pages/index.html')



# Registeration page
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) # Uses the new form
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()

    return render(request, 'pages/register.html', {'form': form})




# --- Login View (custom authentication using email) ---
def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST) # Uses the new form
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # --- CUSTOM EMAIL AUTHENTICATION ---
            try:
                # 1. Find the user by email
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # If email not found, prevent user from being assigned
                user = None 

            # 2. Authenticate using Django's check_password method
            if user is not None and user.check_password(password):
                # 3. If authenticated, log the user in
                login(request, user)
                return redirect('profile')
            else:
                # If email not found or password incorrect, add a non-field error
                form.add_error(None, "Invalid email or password.")
        
    else:
        form = EmailAuthenticationForm()

    # The form now contains either the empty fields or the error messages
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