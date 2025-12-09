from django.conf import settings
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=10, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name="custom_user_set",
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name="custom_permission_set",
        related_query_name="custom_user_permission",
    )

    def __str__(self):
        return self.username


class InstallationBooking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="installations"
    )

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
            ("maintenance", "General Maintenance"),
            ("inverters", "Inverter Installation"),
            ("others", "other installations")
        ]
    )
    notes = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)  # Track completion

    def __str__(self):
        return f"{self.user.username} — {self.installation_type}"

    # Helper method to display status
    def status(self):
        return "Completed" if self.completed else "Pending"
    
