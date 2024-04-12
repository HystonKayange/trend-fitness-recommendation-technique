from django.urls import path
import allauth.account.views

app_name= "user"

urlpatterns = [
    path("logout/", allauth.account.views.logout, name="logout"),
]