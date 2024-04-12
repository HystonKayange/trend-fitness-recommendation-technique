from django.contrib import admin
from django.contrib.auth.models import Group
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_admin']


admin.site.unregister(Group)
admin.site.register(CustomUser, CustomUserAdmin)
