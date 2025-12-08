# website/backends.py

from django.contrib.auth.backends import ModelBackend
# Import your CustomUser model
from .models import CustomUser 

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Look up the user by the 'email' field using the 'username' argument
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            return None
            
        # Standard Django password check
        if user.check_password(password):
            return user
        return None