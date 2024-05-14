from django.contrib import admin
from django.contrib.auth.models import Group
from .models import CustomUser, Profile


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_admin']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'fitness_goal', 'date']
    list_filter = ['fitness_goal', 'tracking_method', 'time_commitment', 'fitness_environment',]
    search_field = ['fitness_goal', 'tracking_method', 'time_commitment', 'fitness_environment',]


admin.site.unregister(Group)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
