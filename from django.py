from django.db import models


class Driver(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    available = models.BooleanField(default=True)
    truck_capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Load(models.Model):
    customer = models.CharField(max_length=100)
    pickup = models.CharField(max_length=200)
    delivery = models.CharField(max_length=200)
    weight = models.IntegerField()
    status = models.CharField(max_length=50, default="Available")

    def __str__(self):
        return self.customer