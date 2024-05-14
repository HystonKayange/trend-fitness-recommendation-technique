from django.urls import path
import allauth.account.views
from .wizards import MyWizard

app_name = "user"

urlpatterns = [
    path("logout/", allauth.account.views.logout, name="logout"),
    #path("profile/<username>", profile_form_view, name="profile_form"),
    path('profile/<username>/', MyWizard.as_view(), name='profile_form'),
]