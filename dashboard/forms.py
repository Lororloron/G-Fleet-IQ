from django import forms

from fleet.models import Company, Customer, Load, Driver, Truck, Trailer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "location"]


class LoadForm(forms.ModelForm):
    class Meta:
        model = Load
        fields = "__all__"


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = "__all__"


class TruckForm(forms.ModelForm):
    class Meta:
        model = Truck
        fields = "__all__"


class TrailerForm(forms.ModelForm):
    class Meta:
        model = Trailer
        fields = "__all__"
    

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"        