from django.urls import path
from .views import list_customers


urlpatterns = [
    path("", list_customers, name="list_customers"),
]
