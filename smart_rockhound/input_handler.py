# Handles user input (GPS coordinates or park name)
import re


def get_user_input() -> dict:
    """
    Prompts the user for GPS coordinates or a park name.
    Returns a dict: {'type': 'coordinates', 'value': (lat, lon)}
    """
    user_input = input(
        "Enter GPS coordinates (lat,lon) or a park name: "
    ).strip()
    # Regex for simple lat,lon (e.g., 34.0522,-118.2437)
    coord_pattern = r"^\s*(-?\d{1,2}\.\d+),\s*(-?\d{1,3}\.\d+)\s*$"
    match = re.match(coord_pattern, user_input)
    if match:
        lat, lon = float(match.group(1)), float(match.group(2))
        return {'type': 'coordinates', 'value': (lat, lon)}
    elif user_input:
        # Park name to lat/lon lookup
        park = user_input.lower().strip()
        if park == 'yosemite national park':
            lat, lon = 37.8651, -119.5383
        elif park == 'central park':
            lat, lon = 40.7829, -73.9654
        else:
            print("Unknown park name. Using default coordinates (0, 0).")
            lat, lon = 0.0, 0.0
        return {'type': 'coordinates', 'value': (lat, lon)}
    else:
        print("Invalid input. Please enter GPS coordinates or a park name.")
        return get_user_input()
