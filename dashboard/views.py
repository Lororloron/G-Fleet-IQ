from django.shortcuts import render, redirect
from fleet.models import Driver, Truck, Trailer, Load, Customer
from .forms import CustomerForm, LoadForm

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
        {
            "drivers": drivers,
        },
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


def trucks(request):
    trucks = Truck.objects.all()

    return render(
        request,
        "dashboard/trucks.html",
        {
            "trucks": trucks,
        },
    )


def loads(request):
    if request.method == "POST":
        form = LoadForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("loads")
    else:
        form = LoadForm()

    loads = Load.objects.all()

    return render(
        request,
        "dashboard/loads.html",
        {
            "loads": loads,
            "form": form,
        },
    )
def trailers(request):
    trailers = Trailer.objects.all()

    return render(
        request,
        "dashboard/trailers.html",
        {
            "trailers": trailers,
        },
    )
def ai_dispatch(request):

    drivers = Driver.objects.all()
    trucks = Truck.objects.all()
    trailers = Trailer.objects.all()
    loads = Load.objects.all()

    recommended_driver = Driver.objects.filter(
        available=True,
        status="Available",
        hours_remaining__gt=0
    ).first()

    recommended_truck = Truck.objects.first()
    recommended_trailer = Trailer.objects.first()
    next_load = Load.objects.first()

    context = {
        "drivers": drivers.count(),
        "trucks": trucks.count(),
        "trailers": trailers.count(),
        "loads": loads.count(),

        "recommended_driver": recommended_driver,
        "recommended_truck": recommended_truck,
        "recommended_trailer": recommended_trailer,
        "next_load": next_load,
    }

    return render(
        request,
        "dashboard/ai_dispatch.html",
        context,
    )
def dispatch_board(request):

    recommended_driver = Driver.objects.filter(
        available=True,
        status="Available"
    ).first()

    recommended_truck = Truck.objects.first()
    recommended_trailer = Trailer.objects.first()

    context = {
        "loads": Load.objects.all(),
        "drivers": Driver.objects.filter(
            available=True,
            status="Available"
        ),
        "trucks": Truck.objects.all(),
        "trailers": Trailer.objects.all(),

        "recommended_driver": recommended_driver,
        "recommended_truck": recommended_truck,
        "recommended_trailer": recommended_trailer,
    }

    return render(
        request,
        "dashboard/dispatch_board.html",
        context,
    )