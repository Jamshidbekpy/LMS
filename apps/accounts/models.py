from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import re

class CustomUserManager(BaseUserManager):
    def create_user(self, username=None, phone=None, email=None, password=None, **extra_fields):
        if not username and not phone:
            raise ValueError("Username yoki telefon raqami talab qilinadi")

        if phone and not re.match(r"^\+998\d{9}$", phone):
            raise ValueError("Telefon raqami faqat '+998xxxxxxxxx' formatida bo‘lishi kerak")
        
        email = self.normalize_email(email) if email else None
        user = self.model(username=username, phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, phone=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(username, phone, email, password, **extra_fields)

class MyUser(AbstractUser):
    ROLE_CHOICES = [
        ("Administrator", "Administrator"),
        ("Student", "Student"),
        ("Teacher", "Teacher"),
        ("Superadmin", "Superadmin"),
    ]
    
    phone = models.CharField(max_length=13, unique=True, null=True, blank=True)  
    email = models.EmailField(unique=True, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES,)

    objects = CustomUserManager()
    
    class Meta:
        verbose_name = "MyUser"
        verbose_name_plural = "MyUsers"

    def __str__(self):
        return f"{self.username} ({self.phone}) - {self.role}"
    
    def save(self, *args, **kwargs):
        if not self.username and self.email:
            self.username = self.email.split("@")[0] 
        super().save(*args, **kwargs)
