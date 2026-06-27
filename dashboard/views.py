from django.shortcuts import render, redirect
from fleet.models import Driver, Truck, Trailer, Load, Customer
from .forms import CustomerForm


def home(request):
    context = {
        "drivers": Driver.objects.count(),
        "trucks": Truck.objects.count(),
        "trailers": Trailer.objects.count(),
        "loads": Load.objects.count(),
        "customers": Customer.objects.count(),
    }

    return render(request, "dashboard/home.html", context)


def drivers(request):
    drivers = Driver.objects.all()

    return render(
        request,
        "dashboard/drivers.html",
        {"drivers": drivers},
    )


def customers(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("customers")
    else:
        form = CustomerForm()

    customers = Customer.objects.all()

    return render(
        request,
        "dashboard/customers.html",
        {
            "customers": customers,
            "form": form,
        },
    )