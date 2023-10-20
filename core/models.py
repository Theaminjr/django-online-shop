from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from datetime import timezone


# Create your models here.

class CustomUserManager(BaseUserManager):

    def create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError(_("The phone number must be set"))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    phone_number = models.CharField(unique=True,max_length=11)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    date_joined = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number
    
    def has_profile(self):
        try:
            return self.profile
        except:
           return False

    

class Profile(models.Model):

    full_name = models.CharField(max_length=100)
    user = models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.phone_number}-profile"


class Address(models.Model):
    
    text = models.TextField()
    postal_code = models.CharField(max_length=10)

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.phone_number}-address-{self.id}"
