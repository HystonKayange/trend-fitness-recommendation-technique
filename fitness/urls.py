from django.urls import path
from .views import index_view, personization_data

app_name = "fitness"

urlpatterns = [
    path("", index_view, name="index"),
    path("personalize/", index_view, name="personalize"),
]