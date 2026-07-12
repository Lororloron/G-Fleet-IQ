from django.shortcuts import render, redirect
from fleet.models import Driver, Truck, Trailer, Load, Customer
from .forms import CustomerForm, LoadForm, DriverForm, TruckForm, TrailerForm

from django.shortcuts import get_object_or_404

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

    recommended_driver = (
    Driver.objects.filter(
        available=True,
        status="Available"
    )
    .order_by("-ai_score")
    .first()
)

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

    available_drivers = Driver.objects.filter(
        available=True,
        status="Available"
    )

    for driver in available_drivers:

        score = 0

        if driver.available:
            score += 40

        if driver.hours_remaining >= 8:
            score += 30
        elif driver.hours_remaining >= 4:
            score += 20
        else:
            score += 10

        if driver.truck:
            score += 20

        driver.ai_score = score
        driver.save()

    recommended_driver = available_drivers.order_by("-ai_score").first()

    recommended_truck = Truck.objects.first()
    recommended_trailer = Trailer.objects.first()

    context = {
        "loads": Load.objects.all(),
        "drivers": available_drivers,
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
def assign_load(request, load_id):

    load = get_object_or_404(Load, id=load_id)

    driver = Driver.objects.filter(
        available=True,
        status="Available"
    ).order_by("-ai_score").first()

    truck = Truck.objects.first()
    trailer = Trailer.objects.first()

    if driver and truck and trailer:

        load.driver = driver
        load.truck = truck
        load.trailer = trailer
        load.status = "Assigned"

        driver.available = False
        driver.status = "Driving"

        load.save()
        driver.save()

    return redirect("dispatch_board")
def add_driver(request):

    if request.method == "POST":
        form = DriverForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("drivers")

    else:
        form = DriverForm()

    return render(
        request,
        "dashboard/add_driver.html",
        {
            "form": form,
        },
    )
def edit_driver(request, driver_id):

    driver = get_object_or_404(Driver, id=driver_id)

    if request.method == "POST":
        form = DriverForm(request.POST, instance=driver)

        if form.is_valid():
            form.save()
            return redirect("drivers")

    else:
        form = DriverForm(instance=driver)

    return render(
    request,
    "dashboard/edit_driver.html",
    {
        "form": form,
        "driver": driver,
    },
)
def add_truck(request):

    if request.method == "POST":
        form = TruckForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("trucks")

    else:
        form = TruckForm()

    return render(
        request,
        "dashboard/add_truck.html",
        {
            "form": form,
        },
    )
def add_trailer(request):

    if request.method == "POST":
        form = TrailerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("trailers")

    else:
        form = TrailerForm()

    return render(
        request,
        "dashboard/add_trailer.html",
        {
            "form": form,
        },
    )
def edit_trailer(request, trailer_id):

    trailer = get_object_or_404(Trailer, id=trailer_id)

    if request.method == "POST":
        form = TrailerForm(request.POST, instance=trailer)

        if form.is_valid():
            form.save()
            return redirect("trailers")

    else:
        form = TrailerForm(instance=trailer)

    return render(
        request,
        "dashboard/edit_trailer.html",
        {
            "form": form,
            "trailer": trailer,
        },
    )
def edit_truck(request, truck_id):

    truck = get_object_or_404(Truck, id=truck_id)

    if request.method == "POST":
        form = TruckForm(request.POST, instance=truck)

        if form.is_valid():
            form.save()
            return redirect("trucks")

    else:
        form = TruckForm(instance=truck)

    return render(
        request,
        "dashboard/edit_truck.html",
        {
            "form": form,
            "truck": truck,
        },
    )
def delete_driver(request, driver_id):

    driver = get_object_or_404(Driver, id=driver_id)

    if request.method == "POST":
        driver.delete()
        return redirect("drivers")

    return render(
        request,
        "dashboard/delete_driver.html",
        {
            "driver": driver,
        },
    )
def delete_truck(request, truck_id):

    truck = get_object_or_404(Truck, id=truck_id)

    if request.method == "POST":
        truck.delete()
        return redirect("trucks")

    return render(
        request,
        "dashboard/delete_truck.html",
        {
            "truck": truck,
        },
    )
def delete_trailer(request, trailer_id):

    trailer = get_object_or_404(Trailer, id=trailer_id)

    if request.method == "POST":
        trailer.delete()
        return redirect("trailers")

    return render(
        request,
        "dashboard/delete_trailer.html",
        {
            "trailer": trailer,
        },
    )
def delete_customer(request, customer_id):

    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == "POST":
        customer.delete()
        return redirect("customers")

    return render(
        request,
        "dashboard/delete_customer.html",
        {
            "customer": customer,
        },
    ) 
def delete_load(request, load_id):

    load = get_object_or_404(Load, id=load_id)

    if request.method == "POST":
        load.delete()
        return redirect("loads")

    return render(
        request,
        "dashboard/delete_load.html",
        {
            "load": load,
        },
    )        
    


    