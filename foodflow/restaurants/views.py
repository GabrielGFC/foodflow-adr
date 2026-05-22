from django.http import JsonResponse
from .models import Restaurant


def list_restaurants(request):
    data = list(Restaurant.objects.filter(is_open=True).values("id", "name", "cuisine"))
    return JsonResponse({"restaurants": data})
