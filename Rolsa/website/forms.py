# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import InstallationBooking
import datetime

# ------------------------------------
# 1. Custom Registration Form (using Email for uniqueness)
# ------------------------------------


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')  # ✔ FIXED

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # email used as username
        if commit:
            user.save()
        return user



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

