from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Permission
from .managers import CustomUserManager
from .utils import *


# Create your models here.
class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name="email",
                              max_length=250, unique=True)
    username = models.CharField(verbose_name="username", max_length=250,
                                unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_all_permissions(self, obj=None):
        # Get permissions based on email and username
        email_permissions = Permission.objects.filter(name=self.email)
        all_permissions = email_permissions

        return all_permissions


class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=True)
    primary_fitness_goal = models.CharField(max_length=100, choices=FITNESS_GOAL)
    medical_history = models.CharField(max_length=100)
    physical_activity_level = models.CharField(max_length=100, choices=PHYSICAL_ACTIVITY_LEVEL)
    nutritional_preferences = models.CharField(max_length=100)
    fitness_environment = models.CharField(max_length=100, choices=FITNESS_ENVIRONMENT)
    tracking_method = models.CharField(max_length=100, choices=TRACKING_METHOD)
    time_commitment = models.CharField(max_length=100, choices=TIME_COMMITMENT)
    challenges = models.TextField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)
