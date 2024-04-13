from django.urls import path
from .views import blog_view

app_name = "blog"

urlpatterns = [
    path("", blog_view, name="blog"),
]