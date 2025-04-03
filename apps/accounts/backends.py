from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class PhoneOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = User.objects.filter(models.Q(username=username) | models.Q(phone=username)).first()
        
        if user and user.check_password(password):
            return user
        return None
