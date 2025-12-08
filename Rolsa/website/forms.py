# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import InstallationBooking, Profile
import datetime

# ------------------------------------
# 1. Custom Registration Form (using Email for uniqueness)
# ------------------------------------


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)  # goes to Profile

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', "")
        user.last_name = self.cleaned_data.get('last_name', "")

        if commit:
            user.save()

            # Create the Profile for the user
            Profile.objects.create(
                user=user,
                phone_number=self.cleaned_data.get('phone_number')
            )

        return user


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email
    

    
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


class InstallationBookingForm(forms.ModelForm):
    installation_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = InstallationBooking
        fields = [
            "full_name",
            "email",
            "phone",
            "address",
            "installation_date",
            "installation_type",
            "notes",
        ]

    def clean_installation_date(self):
        date = self.cleaned_data["installation_date"]
        today = datetime.date.today()

        if date < today:
            raise forms.ValidationError("You cannot select a past date.")

        if date.weekday() in (5, 6):  # No weekends
            raise forms.ValidationError("Installations cannot be booked on weekends.")

        return date
    
# This is the end for the installation

