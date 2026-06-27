from django.db import models


class Driver(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    available = models.BooleanField(default=True)
    truck_capacity = models.IntegerField()

    truck = models.ForeignKey(
        'Truck',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name

class Load(models.Model):
    customer = models.CharField(max_length=100)
    pickup = models.CharField(max_length=200)
    delivery = models.CharField(max_length=200)
    weight = models.IntegerField()
    status = models.CharField(max_length=50, default="Available")

    driver = models.ForeignKey(
        Driver,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    trailer = models.ForeignKey(
        'Trailer',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.customer
      
class Truck(models.Model):
    unit_number = models.CharField(max_length=50)
    capacity = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.unit_number 
class Trailer(models.Model):
    trailer_number = models.CharField(max_length=50)
    loaded = models.BooleanField(default=False)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.trailer_number
class Customer(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name
class Customer(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name        