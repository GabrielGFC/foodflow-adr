from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=120)
    address = models.TextField()
    cuisine = models.CharField(max_length=60)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menu")
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"
