from django.urls import path
from .views import (
    product_view,
    TagListView,
    DetailProductView,
)

app_name = 'product'

urlpatterns = [
    path('tag/<tag>', TagListView.as_view(), name='tag'),
    path('<slug:slug>/', DetailProductView.as_view(), name='detail'),
    path('', product_view, name='product'),
]
