from django.urls import path
from .views import list_restaurants


urlpatterns = [
    path("", list_restaurants, name="list_restaurants"),
]
