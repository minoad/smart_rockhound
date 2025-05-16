# Looks up rock types, terrain, and weather data
import requests


def lookup_data(location):
    """
    Given a location (tuple of lat/lon or park name), return data for:
    - rock_types: list of strings
    - terrain: string (placeholder)
    - weather: string (placeholder)
    """
    if isinstance(location, tuple):
        lat, lon = location
        url = (
            "https://macrostrat.org/api/v2/geologic_units/map?"
            f"lat={lat}&lng={lon}"
        )
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            units = data.get('success', [])
            rock_types = set()
            for unit in units:
                if not isinstance(unit, dict):
                    continue
                liths = unit.get('lithologies', [])
                for lith in liths:
                    if 'lith' in lith:
                        rock_types.add(lith['lith'])
            return {
                'rock_types': list(rock_types) or ['unknown'],
                'terrain': 'unknown',  # Placeholder
                'weather': 'unknown',  # Placeholder
            }
        except requests.RequestException as e:
            return {
                'rock_types': ['error'],
                'terrain': 'unknown',
                'weather': f'API error: {e}',
            }
    elif isinstance(location, str):
        # Assume park name
        if location.lower() == 'yosemite national park':
            return {
                'rock_types': ['granite', 'quartzite'],
                'terrain': 'valley, cliffs',
                'weather': 'clear, 70°F',
            }
        else:
            return {
                'rock_types': ['limestone', 'sandstone'],
                'terrain': 'rolling hills',
                'weather': 'partly cloudy, 65°F',
            }
    else:
        raise ValueError('Invalid location type')
