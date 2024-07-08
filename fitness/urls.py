from django.urls import path
from .views import index_view, search_view, faq_views,  recommendation_view

app_name = "fitness"

urlpatterns = [
    path("", index_view, name="index"),
    path("search/", search_view, name="search"),
    path("faqs/", faq_views, name="faqs"),
    path("recommendation/", recommendation_view, name="recommendation"),
]