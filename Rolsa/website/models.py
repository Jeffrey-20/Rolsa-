from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=10, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"



class InstallationBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="installations")

    full_name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    installation_date = models.DateField()
    installation_type = models.CharField(
        max_length=50,
        choices=[
            ("Solar Panel", "Solar Panel Installation"),
            ("EV Charger", "EV Charger Installation"),
            ("Battery Storage", "Battery Storage Setup"),
            ("Other", "Other"),
        ]
    )

    notes = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — {self.installation_type}"
