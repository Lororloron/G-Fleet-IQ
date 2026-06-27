from django import forms
from fleet.models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "location"]

# Register your models here.
