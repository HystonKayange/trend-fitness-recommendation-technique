from django.urls import path
import allauth.account.views
from .views import profile_form_view

app_name = "user"

urlpatterns = [
    path("logout/", allauth.account.views.logout, name="logout"),
    path("profile/<username>", profile_form_view, name="profile_form"),
]