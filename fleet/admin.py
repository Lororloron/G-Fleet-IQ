from django.contrib import admin
from .models import Truck, Trailer, Driver, Customer, Load


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ("unit_number", "capacity", "active")
    list_filter = ("active",)
    search_fields = ("unit_number",)


@admin.register(Trailer)
class TrailerAdmin(admin.ModelAdmin):
    list_display = (
        "trailer_number",
        "status",
        "location",
        "capacity",
        "available",
        "utilization",
        "last_inspection",
    )
    list_filter = ("status", "available")
    search_fields = ("trailer_number", "location")


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "location",
        "status",
        "available",
        "hours_remaining",
        "truck",
        "ai_score",
        "loads_completed",
    )
    list_filter = ("status", "available")
    search_fields = ("name", "location")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "location",
    )
    search_fields = (
        "name",
        "location",
    )


@admin.register(Load)
class LoadAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "pickup",
        "delivery",
        "weight",
        "distance",
        "status",
        "driver",
        "truck",
        "trailer",
        "rate",
        "profit",
        "profit_per_mile",
    )
    list_filter = (
        "status",
    )
    search_fields = (
        "pickup",
        "delivery",
        "customer__name",
    )