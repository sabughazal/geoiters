"""Utility functions for geoiters package.
"""


EARTH_RADIUS_METERS = 6371000

def haversine(x_min: float, y_min: float, x_max: float, y_max: float) -> float:
    """Calculate the Haversine distance between two geographic points."""
    from math import radians, sin, cos, sqrt, atan2

    R = EARTH_RADIUS_METERS
    dlon = radians(x_max - x_min)
    dlat = radians(y_max - y_min)

    a = sin(dlat / 2)**2 + cos(radians(y_min)) * cos(radians(y_max)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c
