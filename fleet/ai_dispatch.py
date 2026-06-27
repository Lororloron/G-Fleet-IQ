from .models import Driver

def find_best_driver(load):

    available_drivers = Driver.objects.filter(
        available=True
    )

    for driver in available_drivers:

        if (
            driver.truck and
            driver.truck.capacity >= load.weight
        ):
            return driver

    return None