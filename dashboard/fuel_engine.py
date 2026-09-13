import json
import os
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from math import ceil
from decimal import Decimal


DEFAULT_FUEL_PRICE = Decimal("3.75")


def to_decimal(value, default="0"):
    try:
        return Decimal(str(value))
    except (TypeError, ValueError):
        return Decimal(default)


def calculate_fuel_need(miles, mpg):
    miles = to_decimal(miles)
    mpg = to_decimal(mpg)

    if miles <= 0 or mpg <= 0:
        return Decimal("0")

    return miles / mpg


def calculate_fuel_cost(miles, mpg, fuel_price=DEFAULT_FUEL_PRICE):
    gallons = calculate_fuel_need(miles, mpg)
    price = to_decimal(fuel_price, str(DEFAULT_FUEL_PRICE))

    return gallons * price


def calculate_detour_cost(detour_miles, mpg, price_per_gallon):
    detour_gallons = calculate_fuel_need(
        detour_miles,
        mpg,
    )

    return detour_gallons * to_decimal(
        price_per_gallon
    )


def rank_fuel_stops(
    stops,
    trip_miles,
    mpg,
):
    """
    Rank fuel stops by effective trip cost.

    Each stop should contain:
        name
        address
        price_per_gallon
        detour_miles
    """

    mpg = to_decimal(mpg, "7.0")
    trip_miles = to_decimal(trip_miles)

    results = []

    for stop in stops:

        price = to_decimal(
            stop.get(
                "price_per_gallon",
                DEFAULT_FUEL_PRICE,
            ),
            str(DEFAULT_FUEL_PRICE),
        )

        detour_miles = to_decimal(
            stop.get(
                "detour_miles",
                0,
            )
        )

        gallons = calculate_fuel_need(
            trip_miles,
            mpg,
        )

        fuel_cost = gallons * price

        detour_cost = calculate_detour_cost(
            detour_miles,
            mpg,
            price,
        )

        effective_cost = (
            fuel_cost + detour_cost
        )

        results.append({
            **stop,
            "gallons": gallons,
            "fuel_cost": fuel_cost,
            "detour_cost": detour_cost,
            "effective_cost": effective_cost,
        })

    results.sort(
        key=lambda item: item["effective_cost"]
    )

    for index, stop in enumerate(results, start=1):
        stop["rank"] = index

    return results


def get_best_fuel_stop(
    stops,
    trip_miles,
    mpg,
):
    ranked = rank_fuel_stops(
        stops,
        trip_miles,
        mpg,
    )

    return ranked[0] if ranked else None

# ==========================================================
# BEST FUEL STOP
# ==========================================================

def find_best_fuel_stop(
    stations,
    trip_miles,
    mpg,
):
    """
    Return the cheapest practical fuel stop.
    """

    ranked = rank_fuel_stops(
        stations,
        trip_miles,
        mpg,
    )

    if not ranked:
        return None

    return ranked[0]
# ==========================================================
# LIVE HERE DIESEL STATIONS
# ==========================================================

HERE_FUEL_URL = "https://fuel.hereapi.com/v3/stations"

LITERS_PER_GALLON = Decimal("3.785411784")


def _price_per_gallon(price_record):
    """
    Convert HERE fuel price to USD/gallon when possible.
    """

    price = price_record.get("price")

    if price is None:
        return None

    try:
        price = Decimal(str(price))
    except (TypeError, ValueError):
        return None

    currency = price_record.get("currency")
    unit = str(
        price_record.get("unit", "")
    ).lower()

    if currency != "USD":
        return None

    if unit in ("gal", "gallon", "gallons"):
        return price

    if unit in ("l", "liter", "liters"):
        return price * LITERS_PER_GALLON

    return None


def _extract_diesel_price(station):
    """
    Find a diesel price in a HERE station response.

    HERE documents:
        1  = Diesel
        11 = Truck-Diesel
    """

    for price_record in station.get("prices", []):

        fuel_type = str(
            price_record.get("fuelType", "")
        )

        if fuel_type not in ("1", "11"):
            continue

        price = _price_per_gallon(
            price_record
        )

        if price is not None:
            return price, price_record

    return None, None


def _search_here_corridor(points):
    """
    Search HERE for diesel stations inside one
    route corridor.
    """

    api_key = os.getenv(
        "HERE_FUEL_API_KEY"
    )

    if not api_key:
        return []

    if not points:
        return []

    params = urlencode({
        "apiKey": api_key,
        "fuelTypes": "-1",
        "limit": "50",
    })

    url = f"{HERE_FUEL_URL}?{params}"

    body = json.dumps({
        "corridor": points,
        "width": 5000,
    }).encode("utf-8")

    request = Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "G-Fleet-IQ/1.0",
        },
        method="POST",
    )

    try:

        with urlopen(
            request,
            timeout=20,
        ) as response:

            return json.loads(
                response.read().decode(
                    "utf-8"
                )
            ).get("stations", [])

    except Exception as e:
        print("HERE FUEL ERROR:", e)
        return []


def get_live_diesel_stops(
    geometry,
    trip_miles,
):     
    """
    Find live diesel stations along the route.

    geometry must be the GeoJSON geometry
    returned by OSRM.

    Returns normalized station records.
    """

    if not geometry:
        return []

    coordinates = geometry.get(
        "coordinates",
        []
    )

    if len(coordinates) < 2:
        return []

    trip_miles = float(
        trip_miles or 0
    )

    # HERE corridor searches have an area limit.
    # Break long routes into practical chunks.
    chunk_count = max(
        1,
        ceil(trip_miles / 450),
    )

    chunk_size = max(
        2,
        ceil(
            len(coordinates)
            / chunk_count
        ),
    )

    stations = []

    for start in range(
        0,
        len(coordinates),
        chunk_size,
    ):

        chunk = coordinates[
            start:start + chunk_size
        ]

        if len(chunk) < 2:
            continue

        # GeoJSON = [longitude, latitude]
        points = [
            {
                "lat": point[1],
                "lng": point[0],
            }
            for point in chunk
            if len(point) >= 2
        ]

        raw_stations = (
            _search_here_corridor(
                points
            )
        )

        for station in raw_stations:

            price, price_record = (
                _extract_diesel_price(
                    station
                )
            )

            if price is None:
                continue

            address = station.get(
                "address",
                {}
            )

            stations.append({
                "id": station.get("id"),
                "name": station.get(
                    "name",
                    "Unknown Station",
                ),
                "address": address.get(
                    "label",
                    "",
                ),
                "price_per_gallon": price,
                "detour_miles": 0,
                "source": "HERE",
                "price_updated": (
                    price_record.get(
                        "modified"
                    )
                    if price_record
                    else None
                ),
            })

    # Remove duplicates
    unique = {}

    for station in stations:

        station_id = station.get("id")

        if station_id:
            unique[station_id] = station

    return list(unique.values())
# ==========================================================
# FUEL PROVIDERS
# ==========================================================

FUEL_PROVIDERS = [
    "Pilot",
    "Flying J",
    "Love's",
    "TA",
    "Petro",
    "Speedway",
    "Wawa",
    "Q Stop",
    "QuikTrip",
]

def normalize_fuel_station(
    brand,
    name,
    address,
    price_per_gallon,
    detour_miles=0,
):
    """
    Convert any fuel provider's station data into
    the standard G Fleet IQ format.
    """

    return {
        "brand": brand,
        "name": name,
        "address": address,
        "price_per_gallon": price_per_gallon,
        "detour_miles": detour_miles,
    }


def get_supported_fuel_providers():
    return FUEL_PROVIDERS
# ==========================================================
# PILOT FUEL PRICE SOURCE
# ==========================================================

PILOT_FUEL_PRICES_URL = "https://pilotcompany.com/fuel-prices"


def get_pilot_diesel_stations():
    """
    Get Pilot/Flying J diesel station records.

    This function is intentionally separate from the AI
    ranking engine so the provider can be changed later.
    """

    return []
# ==========================================================
# PILOT / FLYING J FUEL DATA
# ==========================================================

def normalize_pilot_station(station):
    """
    Convert a Pilot/Flying J station result into
    the standard G Fleet IQ fuel-station format.
    """

    return normalize_fuel_station(
        brand=station.get("brand", "Pilot"),
        name=station.get("name", "Pilot/Flying J"),
        address=station.get("address", ""),
        price_per_gallon=station.get(
            "diesel_price"
        ),
        detour_miles=station.get(
            "detour_miles",
            0,
        ),
    )
# ==========================================================
# LOVE'S PROVIDER
# ==========================================================

def normalize_loves_station(station):
    """
    Convert a Love's station result into the standard
    G Fleet IQ fuel-station format.
    """

    return normalize_fuel_station(
        brand="Love's",
        name=station.get("name", "Love's Travel Stop"),
        address=station.get("address", ""),
        price_per_gallon=station.get(
            "diesel_price"
        ),
        detour_miles=station.get(
            "detour_miles",
            0,
        ),
    )
    # ==========================================================
# TA / PETRO PROVIDER
# ==========================================================

def normalize_ta_petro_station(station):
    """
    Convert a TA or Petro station result into the
    standard G Fleet IQ fuel-station format.
    """

    return normalize_fuel_station(
        brand=station.get("brand", "TA"),
        name=station.get(
            "name",
            "TA/Petro Travel Center",
        ),
        address=station.get(
            "address",
            "",
        ),
        price_per_gallon=station.get(
            "diesel_price"
        ),
        detour_miles=station.get(
            "detour_miles",
            0,
        ),
    )
# ==========================================================
# QUikTrip (QT) PROVIDER
# ==========================================================

def normalize_qt_station(station):
    """
    Convert a QuikTrip station result into the
    standard G Fleet IQ fuel-station format.
    """

    return normalize_fuel_station(
        brand="QuikTrip",
        name=station.get(
            "name",
            "QuikTrip",
        ),
        address=station.get(
            "address",
            "",
        ),
        price_per_gallon=station.get(
            "diesel_price"
        ),
        detour_miles=station.get(
            "detour_miles",
            0,
        ),
    )