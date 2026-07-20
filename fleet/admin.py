from django.contrib import admin
from .models import Company, Truck, Trailer, Driver, Customer, Load


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "dot_number",
        "mc_number",
        "email",
        "phone",
        "active",
    )
    list_filter = ("active",)
    search_fields = (
        "name",
        "dot_number",
        "mc_number",
    )


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = (
        "unit_number",
        "capacity",
        "active",
        "company",
    )
    list_filter = (
        "active",
        "company",
    )
    search_fields = (
        "unit_number",
    )


@admin.register(Trailer)
class TrailerAdmin(admin.ModelAdmin):
    list_display = (
        "trailer_number",
        "company",
        "status",
        "location",
        "capacity",
        "available",
        "utilization",
        "last_inspection",
    )
    list_filter = (
        "company",
        "status",
        "available",
    )
    search_fields = (
        "trailer_number",
        "location",
    )


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "company",
        "location",
        "status",
        "available",
        "hours_remaining",
        "truck",
        "ai_score",
        "loads_completed",
    )
    list_filter = (
        "company",
        "status",
        "available",
    )
    search_fields = (
        "name",
        "location",
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "company",
        "location",
    )
    list_filter = (
        "company",
    )
    search_fields = (
        "name",
        "location",
    )


@admin.register(Load)
class LoadAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "company",
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
        "company",
        "status",
    )
    search_fields = (
        "pickup",
        "delivery",
        "customer__name",
    )