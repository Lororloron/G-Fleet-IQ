# ==========================================================
# G FLEET IQ - FUEL PROVIDERS
# ==========================================================

QT_BASE_URL = "https://locations.quiktrip.com"


def normalize_qt_location(location):
    """
    Convert a QuikTrip location into the standard
    G Fleet IQ fuel-station format.
    """

    fuel_types = location.get("fuel_types", [])

    truck_diesel = any(
        "Truck Diesel" in fuel
        for fuel in fuel_types
    )

    return {
        "brand": "QuikTrip",
        "name": location.get(
            "name",
            "QuikTrip",
        ),
        "address": location.get(
            "address",
            "",
        ),
        "price_per_gallon": location.get(
            "diesel_price"
        ),
        "detour_miles": location.get(
            "detour_miles",
            0,
        ),
        "truck_diesel": truck_diesel,
        "source": "QuikTrip",
    }
# ==========================================================
# QUIKTRIP TRUCK-DIESEL FILTER
# ==========================================================

def is_qt_truck_diesel(location):
    """
    Return True only when the QT location explicitly
    offers Truck Diesel.
    """

    fuel_types = location.get(
        "fuel_types",
        []
    )

    return any(
        str(fuel).lower() == "truck diesel"
        for fuel in fuel_types
    )


def normalize_qt_truck_stop(location):
    """
    Normalize a QuikTrip location for G Fleet IQ.

    Only locations offering Truck Diesel are accepted.
    """

    if not is_qt_truck_diesel(location):
        return None

    station = normalize_qt_location(location)

    station["truck_diesel"] = True

    return station
# ==========================================================
# REAL QUIKTRIP LOCATION CANDIDATES
# ==========================================================

def get_qt_truck_diesel_candidates(locations):
    """
    Keep only QuikTrip locations that offer Truck Diesel.

    Expected location format:
    {
        "name": "...",
        "address": "...",
        "fuel_types": ["Auto Diesel", "Truck Diesel"],
        "diesel_price": None,
        "detour_miles": 0,
    }
    """

    candidates = []

    for location in locations:

        station = normalize_qt_truck_stop(
            location
        )

        if station is None:
            continue

        candidates.append(
            station
        )

    return candidates
# ==========================================================
# QT ROUTE CANDIDATE FILTER
# ==========================================================

def get_qt_route_candidates(
    locations,
    max_detour_miles=5.0,
):
    """
    Keep QT Truck Diesel locations that are within the
    requested detour distance from the route.

    Each location should already contain:
        truck_diesel
        detour_miles
    """

    candidates = []

    for location in locations:

        station = normalize_qt_truck_stop(
            location
        )

        if station is None:
            continue

        detour = float(
            station.get(
                "detour_miles",
                0,
            ) or 0
        )

        if detour <= max_detour_miles:
            candidates.append(
                station
            )

    candidates.sort(
        key=lambda station: float(
            station.get(
                "detour_miles",
                0,
            ) or 0
        )
    )

    return candidates