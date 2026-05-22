from django.http import JsonResponse
from .models import Customer


def list_customers(request):
    data = list(Customer.objects.values("id", "name", "email", "phone"))
    return JsonResponse({"customers": data})
