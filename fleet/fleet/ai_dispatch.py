from .models import Driver

def find_best_driver(load):

    drivers = Driver.objects.filter(
        available=True
    )

    best_driver = None

    for driver in drivers:

        if driver.truck and driver.truck.capacity >= load.weight:
            best_driver = driver
            break

    return best_driver