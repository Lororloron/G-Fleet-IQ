from django import forms

from fleet.models import (
    Company,
    Customer,
    Load,
    Driver,
    Truck,
    Trailer,
)


# ==========================================================
# CUSTOMER FORM
# ==========================================================

class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = [
            "name",
            "location",
        ]


# ==========================================================
# LOAD FORM
# ==========================================================

class LoadForm(forms.ModelForm):

    pickup_datetime = forms.DateTimeField(
        input_formats=[
            "%m/%d/%Y %I:%M %p"
        ],
        widget=forms.TextInput(
            attrs={
                "placeholder": "MM/DD/YYYY HH:MM AM/PM",
            }
        ),
    )

    delivery_datetime = forms.DateTimeField(
        input_formats=[
            "%m/%d/%Y %I:%M %p"
        ],
        widget=forms.TextInput(
            attrs={
                "placeholder": "MM/DD/YYYY HH:MM AM/PM",
            }
        ),
    )

    class Meta:
        model = Load

        fields = [
            "customer",
            "pickup",
            "delivery",
            "pickup_datetime",
            "delivery_datetime",
            "weight",
            "miles",
            "rate",
            "equipment_type",
            "priority",
            "distance",
            "fuel_cost",
            "driver_pay",
            "tolls",
            "maintenance_cost",
            "insurance_cost",
        ]


# ==========================================================
# DRIVER FORM
# ==========================================================

class DriverForm(forms.ModelForm):

    class Meta:
        model = Driver

        fields = "__all__"


# ==========================================================
# TRUCK FORM
# ==========================================================

class TruckForm(forms.ModelForm):

    class Meta:
        model = Truck

        fields = "__all__"


# ==========================================================
# TRAILER FORM
# ==========================================================

class TrailerForm(forms.ModelForm):

    class Meta:
        model = Trailer

        fields = "__all__"


# ==========================================================
# COMPANY FORM
# ==========================================================

class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company

        fields = "__all__"