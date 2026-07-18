from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg

from fleet.models import Driver, Truck, Trailer, Load, Customer
from .forms import (
    CustomerForm,
    LoadForm,
    DriverForm,
    TruckForm,
    TrailerForm,
)


# ==========================================================
# HOME
# ==========================================================

def home(request):

    average_ai_score = (
        Driver.objects.aggregate(Avg("ai_score"))["ai_score__avg"] or 0
    )

    recommended_driver = (
        Driver.objects.filter(
            available=True,
            status="Available",
        )
        .order_by("-ai_score")
        .first()
    )

    context = {
        "drivers": Driver.objects.count(),
        "trucks": Truck.objects.count(),
        "trailers": Trailer.objects.count(),
        "loads": Load.objects.count(),
        "customers": Customer.objects.count(),

        "available_drivers": Driver.objects.filter(
            available=True
        ).count(),

        "assigned_loads": Load.objects.filter(
            status="Assigned"
        ).count(),

        "available_trucks": Truck.objects.count(),
        "available_trailers": Trailer.objects.count(),

        "available_loads": Load.objects.filter(
            status="Available"
        ).count(),

        "completed_loads": Load.objects.filter(
            status="Assigned"
        ).count(),

        "average_ai_score": average_ai_score,
        "recommended_driver": recommended_driver,
        "top_drivers": Driver.objects.order_by("-ai_score")[:5],
        "recent_loads": Load.objects.order_by("-id")[:5],
    }

    return render(
        request,
        "dashboard/home.html",
        context,
    )


# ==========================================================
# DRIVERS
# ==========================================================

def drivers(request):

    return render(
        request,
        "dashboard/drivers.html",
        {
            "drivers": Driver.objects.all(),
        },
    )


# ==========================================================
# CUSTOMERS
# ==========================================================

def customers(request):

    if request.method == "POST":

        form = CustomerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("customers")

    else:

        form = CustomerForm()

    return render(
        request,
        "dashboard/customers.html",
        {
            "customers": Customer.objects.all(),
            "form": form,
        },
    )


# ==========================================================
# TRUCKS
# ==========================================================

def trucks(request):

    return render(
        request,
        "dashboard/trucks.html",
        {
            "trucks": Truck.objects.all(),
        },
    )


# ==========================================================
# TRAILERS
# ==========================================================

def trailers(request):

    return render(
        request,
        "dashboard/trailers.html",
        {
            "trailers": Trailer.objects.all(),
        },
    )


# ==========================================================
# LOADS
# ==========================================================

def loads(request):

    if request.method == "POST":

        form = LoadForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("loads")

    else:

        form = LoadForm()

    return render(
        request,
        "dashboard/loads.html",
        {
            "loads": Load.objects.all(),
            "form": form,
        },
    )
# ==========================================================
# AI DISPATCH
# ==========================================================

def ai_dispatch(request):

    recommended_driver = (
        Driver.objects.filter(
            available=True,
            status="Available",
        )
        .order_by("-ai_score")
        .first()
    )

    recommended_truck = (
        Truck.objects.filter(active=True).first()
    )

    recommended_trailer = (
        Trailer.objects.filter(loaded=False).first()
    )

    next_load = (
        Load.objects.filter(status="Available").first()
    )

    context = {
        "drivers": Driver.objects.count(),
        "trucks": Truck.objects.count(),
        "trailers": Trailer.objects.count(),
        "loads": Load.objects.count(),

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


# ==========================================================
# DISPATCH BOARD
# ==========================================================

def dispatch_board(request):

    available_drivers = Driver.objects.filter(
        available=True,
        status="Available",
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
        driver.save(update_fields=["ai_score"])

    recommended_driver = (
        available_drivers.order_by("-ai_score").first()
    )

    recommended_truck = (
        Truck.objects.filter(active=True).first()
    )

    recommended_trailer = (
        Trailer.objects.filter(loaded=False).first()
    )

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


# ==========================================================
# ASSIGN LOAD
# ==========================================================

def assign_load(request, load_id):

    load = get_object_or_404(
        Load,
        id=load_id,
    )

    driver = (
        Driver.objects.filter(
            available=True,
            status="Available",
        )
        .order_by("-ai_score")
        .first()
    )

    truck = (
        Truck.objects.filter(active=True).first()
    )

    trailer = (
        Trailer.objects.filter(loaded=False).first()
    )

    if driver and truck and trailer:

        load.driver = driver
        load.truck = truck
        load.trailer = trailer
        load.status = "Assigned"

        driver.available = False
        driver.status = "Driving"

        trailer.loaded = True

        driver.save()
        trailer.save()
        load.save()

    return redirect("dispatch_board")
# ==========================================================
# DRIVER FUNCTIONS
# ==========================================================

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

    driver = get_object_or_404(
        Driver,
        id=driver_id,
    )

    if request.method == "POST":

        form = DriverForm(
            request.POST,
            instance=driver,
        )

        if form.is_valid():
            form.save()
            return redirect("drivers")

    else:

        form = DriverForm(
            instance=driver,
        )

    return render(
        request,
        "dashboard/edit_driver.html",
        {
            "driver": driver,
            "form": form,
        },
    )


def delete_driver(request, driver_id):

    driver = get_object_or_404(
        Driver,
        id=driver_id,
    )

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


# ==========================================================
# TRUCK FUNCTIONS
# ==========================================================

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


def edit_truck(request, truck_id):

    truck = get_object_or_404(
        Truck,
        id=truck_id,
    )

    if request.method == "POST":

        form = TruckForm(
            request.POST,
            instance=truck,
        )

        if form.is_valid():
            form.save()
            return redirect("trucks")

    else:

        form = TruckForm(
            instance=truck,
        )

    return render(
        request,
        "dashboard/edit_truck.html",
        {
            "truck": truck,
            "form": form,
        },
    )


def delete_truck(request, truck_id):

    truck = get_object_or_404(
        Truck,
        id=truck_id,
    )

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


# ==========================================================
# TRAILER FUNCTIONS
# ==========================================================

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

    trailer = get_object_or_404(
        Trailer,
        id=trailer_id,
    )

    if request.method == "POST":

        form = TrailerForm(
            request.POST,
            instance=trailer,
        )

        if form.is_valid():
            form.save()
            return redirect("trailers")

    else:

        form = TrailerForm(
            instance=trailer,
        )

    return render(
        request,
        "dashboard/edit_trailer.html",
        {
            "trailer": trailer,
            "form": form,
        },
    )


def delete_trailer(request, trailer_id):

    trailer = get_object_or_404(
        Trailer,
        id=trailer_id,
    )

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


# ==========================================================
# CUSTOMER FUNCTIONS
# ==========================================================

def delete_customer(request, customer_id):

    customer = get_object_or_404(
        Customer,
        id=customer_id,
    )

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


# ==========================================================
# LOAD FUNCTIONS
# ==========================================================

def delete_load(request, load_id):

    load = get_object_or_404(
        Load,
        id=load_id,
    )

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