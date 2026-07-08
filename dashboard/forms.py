from django import forms
from fleet.models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "location"]
from django import forms
from fleet.models import Customer, Load


class LoadForm(forms.ModelForm):
    class Meta:
        model = Load
        fields = "__all__" 
from fleet.models import Driver

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = "__all__"               