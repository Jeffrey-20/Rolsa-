# website/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, InstallationBooking # Import CustomUser instead of Profile
import datetime

# ------------------------------------
# A. Custom Registration Form
# ------------------------------------
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    
    # Custom fields
    phone_number = forms.CharField(required=False)
    address = forms.CharField(required=False)
    postcode = forms.CharField(required=False)

class CustomUserCreationForm(UserCreationForm):
    # Field definitions remain the same
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=False)
    address = forms.CharField(required=False)
    postcode = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'phone_number', 
            'address', 
            'postcode', 
            
           
        )

    # Clean and save methods remain correct for CustomUser logic
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
        return user
    


# ------------------------------------
# B. Email Authentication Form
# ------------------------------------
class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput
    )


# ------------------------------------
# C. Installation Booking Form
# ------------------------------------
class InstallationBookingForm(forms.ModelForm):
    installation_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = InstallationBooking
        fields = [
            "full_name", "email", "phone", "address", 
            "installation_date", "installation_type", "notes"
        ]

    def clean_installation_date(self):
        date = self.cleaned_data["installation_date"]
        today = datetime.date.today()

        if date < today:
            raise forms.ValidationError("You cannot select a past date.")

        if date.weekday() in (5, 6): # Saturday/Sunday
            raise forms.ValidationError("Installations cannot be booked on weekends.")

        return date