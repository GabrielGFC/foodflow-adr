from django.urls import path
from .views import list_orders, create_order


urlpatterns = [
    path("", list_orders, name="list_orders"),
    path("create/", create_order, name="create_order"),
]
