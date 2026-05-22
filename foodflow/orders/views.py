import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Order, OrderItem
from restaurants.models import MenuItem


def list_orders(request):
    data = list(Order.objects.values("id", "customer_id", "restaurant_id", "status", "total"))
    return JsonResponse({"orders": data})


@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    payload = json.loads(request.body)
    order = Order.objects.create(
        customer_id=payload["customer_id"],
        restaurant_id=payload["restaurant_id"],
    )
    total = 0
    for item in payload["items"]:
        menu = MenuItem.objects.get(pk=item["menu_item_id"])
        OrderItem.objects.create(
            order=order,
            menu_item=menu,
            quantity=item["quantity"],
            unit_price=menu.price,
        )
        total += menu.price * item["quantity"]
    order.total = total
    order.save()
    return JsonResponse({"id": order.id, "total": str(order.total)}, status=201)
