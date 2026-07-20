from django.db import models
class Company(models.Model):
    name = models.CharField(max_length=200)
    dot_number = models.CharField(max_length=50, blank=True)
    mc_number = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Truck(models.Model):
    unit_number = models.CharField(max_length=50)
    capacity = models.IntegerField()
    active = models.BooleanField(default=True)

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="trucks"
    )

    def __str__(self):
        return self.unit_number

class Trailer(models.Model):
    STATUS_CHOICES = [
        ("Empty", "Empty"),
        ("Loaded", "Loaded"),
        ("Maintenance", "Maintenance"),
        ("Out of Service", "Out of Service"),
    ]

    trailer_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Empty"
    )
    location = models.CharField(max_length=200)
    capacity = models.IntegerField(default=53000)
    available = models.BooleanField(default=True)
    utilization = models.FloatField(default=0)
    last_inspection = models.DateField(
        null=True,
        blank=True
    )
    company = models.ForeignKey(
    Company,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    related_name="trailers"
)

    def __str__(self):
        return self.trailer_number


class Driver(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    available = models.BooleanField(default=True)
    truck_capacity = models.IntegerField()

    status = models.CharField(
        max_length=20,
        default="Available"
    )

    hours_remaining = models.IntegerField(default=11)
    phone = models.CharField(max_length=20, blank=True)
    ai_score = models.IntegerField(default=0)
    miles_today = models.IntegerField(default=0)
    loads_completed = models.IntegerField(default=0)
    fuel_efficiency = models.FloatField(default=0)

    truck = models.ForeignKey(
        Truck,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    company = models.ForeignKey(
    Company,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    related_name="drivers"
)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    company = models.ForeignKey(
    Company,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    related_name="customers"
)

    def __str__(self):
        return self.name


class Load(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="loads"
    )

    pickup = models.CharField(max_length=200)
    delivery = models.CharField(max_length=200)
    weight = models.IntegerField()
    distance = models.IntegerField(default=0)

    rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    fuel_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    driver_pay = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    tolls = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    maintenance_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    insurance_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    profit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    profit_per_mile = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=50,
        default="Available"
    )

    driver = models.ForeignKey(
        Driver,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    truck = models.ForeignKey(
        Truck,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    trailer = models.ForeignKey(
        Trailer,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    company = models.ForeignKey(
    Company,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    related_name="loads"
)

    def __str__(self):
        return f"{self.customer.name} | {self.pickup} → {self.delivery}"