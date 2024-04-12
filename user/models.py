from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Permission
from .managers import CustomUserManager


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
