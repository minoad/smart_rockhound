import builtins
import unittest
from unittest.mock import patch

import pytest
import requests

from smart_rockhound.data_lookup import lookup_data
from smart_rockhound.input_handler import get_user_input


class TestInputHandler(unittest.TestCase):
    def test_valid_coordinates(self):
        with patch('builtins.input', return_value='34.0522,-118.2437'):
            result = get_user_input()
            self.assertEqual(result['type'], 'coordinates')
            self.assertEqual(result['value'][0], 34.0522)
            self.assertEqual(result['value'][1], -118.2437)

    def test_valid_coordinates_with_spaces(self):
        with patch('builtins.input', return_value=' 34.0522, -118.2437 '):
            result = get_user_input()
            self.assertEqual(result['type'], 'coordinates')
            self.assertEqual(result['value'][0], 34.0522)
            self.assertEqual(result['value'][1], -118.2437)

    def test_valid_park_name(self):
        with patch('builtins.input', return_value='Yosemite National Park'):
            result = get_user_input()
            self.assertEqual(result['type'], 'park')
            self.assertEqual(result['value'], 'Yosemite National Park')

    def test_invalid_then_valid(self):
        with patch('builtins.input', side_effect=['', '34.0522,-118.2437']):
            result = get_user_input()
            self.assertEqual(result['type'], 'coordinates')
            self.assertEqual(result['value'][0], 34.0522)
            self.assertEqual(result['value'][1], -118.2437)


@pytest.mark.parametrize(
    "mock_input,expected",
    [
        (
            "34.0522,-118.2437",
            {'type': 'coordinates', 'value': (34.0522, -118.2437)}
        ),
        (
            " 34.0522, -118.2437 ",
            {'type': 'coordinates', 'value': (34.0522, -118.2437)}
        ),
        (
            "Yosemite National Park",
            {'type': 'park', 'value': "Yosemite National Park"}
        ),
        (
            "Central Park",
            {'type': 'park', 'value': "Central Park"}
        ),
    ]
)
def test_get_user_input(monkeypatch, mock_input, expected):
    monkeypatch.setattr(builtins, "input", lambda _: mock_input)
    result = get_user_input()
    assert result == expected


def test_get_user_input_invalid_then_valid(monkeypatch):
    # Simulate invalid input followed by valid coordinates
    inputs = iter(["", "34.0522,-118.2437"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    result = get_user_input()
    assert result == {'type': 'coordinates', 'value': (34.0522, -118.2437)}


def test_lookup_data_coordinates(monkeypatch):
    # Mock requests.get to return a fake Macrostrat response
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                'success': [
                    {'lithologies': [{'lith': 'granite'}, {'lith': 'basalt'}]},
                    {'lithologies': [{'lith': 'sandstone'}]},
                ]
            }
    monkeypatch.setattr(requests, 'get', lambda *a, **kw: MockResponse())
    from smart_rockhound.data_lookup import lookup_data
    result = lookup_data((34.0522, -118.2437))
    assert 'granite' in result['rock_types']
    assert 'basalt' in result['rock_types']
    assert 'sandstone' in result['rock_types']
    assert result['terrain'] == 'unknown'
    assert result['weather'] == 'unknown'


def test_lookup_data_coordinates_api_error(monkeypatch):
    # Mock requests.get to raise a RequestException
    def mock_get(*args, **kwargs):
        raise requests.RequestException("API error")
    monkeypatch.setattr(requests, 'get', mock_get)
    from smart_rockhound.data_lookup import lookup_data
    result = lookup_data((0, 0))
    assert result['rock_types'] == ['error']
    assert result['terrain'] == 'unknown'
    assert 'API error' in result['weather']


def test_lookup_data_park_name():
    from smart_rockhound.data_lookup import lookup_data
    yosemite = lookup_data('Yosemite National Park')
    assert yosemite['rock_types'] == ['granite', 'quartzite']
    assert yosemite['terrain'] == 'valley, cliffs'
    assert yosemite['weather'] == 'clear, 70°F'
    other = lookup_data('Central Park')
    assert other['rock_types'] == ['limestone', 'sandstone']
    assert other['terrain'] == 'rolling hills'
    assert other['weather'] == 'partly cloudy, 65°F'


def test_lookup_data_invalid():
    import pytest
    with pytest.raises(ValueError):
        lookup_data(12345)


if __name__ == '__main__':
    unittest.main()
