import json
from math import ceil
from urllib.parse import quote
from urllib.request import Request, urlopen


OSRM_URL = "https://router.project-osrm.org/route/v1/driving"


def get_road_route(
    start_lat,
    start_lon,
    end_lat,
    end_lon,
):
    """
    Get real road distance, driving time, and route geometry using OSRM.

    Returns:
        {
            "miles": ...,
            "drive_hours": ...,
            "geometry": ...,
        }

    Returns None if routing fails.
    """

    if None in (
        start_lat,
        start_lon,
        end_lat,
        end_lon,
    ):
        return None

    coordinates = (
        f"{start_lon},{start_lat};"
        f"{end_lon},{end_lat}"
    )

    url = (
        f"{OSRM_URL}/{quote(coordinates, safe=',;')}"
        "?overview=full&geometries=geojson"
    )

    request = Request(
        url,
        headers={
            "User-Agent": "G-Fleet-IQ/1.0"
        },
    )

    try:

        with urlopen(
            request,
            timeout=10,
        ) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

        if data.get("code") != "Ok":
            return None

        route = data["routes"][0]

        distance_meters = route["distance"]
        duration_seconds = route["duration"]

        miles = round(
            distance_meters / 1609.344,
            1,
        )

        drive_hours = round(
            duration_seconds / 3600,
            1,
        )

        return {
            "miles": miles,
            "drive_hours": drive_hours,
            "geometry": route.get("geometry"),
        }

    except Exception:
        return None


def calculate_route(load):
    """
    Calculate the actual road route for a load.

    Uses pickup -> delivery GPS coordinates when available.
    Falls back to the stored miles when routing is unavailable.
    """

    route = get_road_route(
        load.pickup_latitude,
        load.pickup_longitude,
        load.delivery_latitude,
        load.delivery_longitude,
    )

    if route:

        miles = route["miles"]
        drive_hours = route["drive_hours"]

    else:

        miles = load.miles or load.distance or 0

        average_speed = 60

        drive_hours = round(
            miles / average_speed,
            1,
        )

    mpg = 7
    fuel_price = 3.75

    gallons = (
        round(miles / mpg, 1)
        if miles > 0
        else 0
    )

    fuel_cost = round(
        gallons * fuel_price,
        2,
    )

    truck_stops = max(
        1,
        ceil(miles / 500),
    )

    return {
    "miles": miles,
    "drive_hours": drive_hours,
    "fuel_cost": fuel_cost,
    "truck_stops": truck_stops,
    "geometry": route.get("geometry") if route else None,
}