import json
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.core.cache import cache


NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

USER_AGENT = (
    "G-Fleet-IQ/1.0 "
    "(fleet dispatch development application)"
)

_last_request_time = 0.0


def geocode_address(address):
    """
    Convert a street/city/state address into latitude/longitude.

    Results are cached so the same address is not repeatedly
    sent to the geocoding provider.
    """

    global _last_request_time

    if not address:
        return None

    address = " ".join(address.strip().split())

    cache_key = f"g_fleet_iq_geocode:{address.lower()}"

    cached = cache.get(cache_key)

    if cached:
        return cached

    # Respect the public Nominatim service's request limit.
    elapsed = time.monotonic() - _last_request_time

    if elapsed < 1.0:
        time.sleep(1.0 - elapsed)

    params = urlencode({
        "q": address,
        "format": "jsonv2",
        "limit": 1,
        "countrycodes": "us",
        "addressdetails": 1,
    })

    request = Request(
        f"{NOMINATIM_URL}?{params}",
        headers={
            "User-Agent": USER_AGENT,
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

        _last_request_time = time.monotonic()

    except Exception:
        return None

    if not data:
        return None

    result = {
        "latitude": float(data[0]["lat"]),
        "longitude": float(data[0]["lon"]),
        "display_name": data[0].get(
            "display_name",
            address,
        ),
    }

    # Cache for 30 days.
    cache.set(
        cache_key,
        result,
        60 * 60 * 24 * 30,
    )

    return result