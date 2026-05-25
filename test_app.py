import pytest
from unittest.mock import patch, MagicMock
from app import (
    get_temperature,
    get_wind_speed,
    get_weather_description,
    celsius_to_fahrenheit,
    is_strong_wind,
    classify_temperature,
    get_weather,
)


# ─────────────────────────────────────────────
MOCK_RESPONSE = {
    "current_weather": {
        "temperature": 22.5,
        "windspeed": 18.3,
        "winddirection": 120,
        "weathercode": 2,
        "is_day": 1,
        "time": "2026-05-25T12:00"
    },
    "hourly": {
        "relative_humidity_2m": [65, 67, 70]
    }
}



def test_get_weather_returns_valid_response():
    """
    Verifies that the Open-Meteo API returns a valid JSON response
    containing 'current_weather' for Melbourne, Australia.
    """
    data = get_weather(latitude=-37.8136, longitude=144.9631)
    assert "current_weather" in data, "Response must contain 'current_weather' key"
    assert "temperature" in data["current_weather"], "current_weather must include temperature"
    assert "windspeed" in data["current_weather"], "current_weather must include windspeed"


def test_get_temperature_returns_correct_value():
    """
    Verifies that temperature is correctly extracted from the API response.
    """
    temp = get_temperature(MOCK_RESPONSE)
    assert temp == 22.5

def test_get_wind_speed_returns_correct_value():
    """
    Verifies that wind speed is correctly extracted from the API response.
    """
    wind = get_wind_speed(MOCK_RESPONSE)
    assert wind == 18.3


def test_celsius_to_fahrenheit_conversion():
    """
    Verifies correct Celsius to Fahrenheit conversion for known values.
    0°C → 32°F, 100°C → 212°F, 22.5°C → 72.5°F
    """
    assert celsius_to_fahrenheit(0) == 32.0
    assert celsius_to_fahrenheit(100) == 212.0
    assert celsius_to_fahrenheit(22.5) == 72.5


def test_weather_description_known_codes():
    """
    Verifies that WMO weather codes are correctly mapped to descriptions.
    """
    assert get_weather_description(0) == "Clear sky"
    assert get_weather_description(63) == "Moderate rain"
    assert get_weather_description(95) == "Thunderstorm"
    assert get_weather_description(999) == "Unknown condition"

def test_is_strong_wind():
    """
    Verifies wind classification: above 50 km/h is strong wind.
    """
    assert is_strong_wind(80) is True
    assert is_strong_wind(50) is False   # exactly 50 is NOT strong
    assert is_strong_wind(10) is False


def test_classify_temperature():
    """
    Verifies temperature is correctly classified into human-readable categories.
    """
    assert classify_temperature(-5)  == "Freezing"
    assert classify_temperature(5)   == "Cold"
    assert classify_temperature(15)  == "Mild"
    assert classify_temperature(25)  == "Warm"
    assert classify_temperature(35)  == "Hot"

def test_celsius_to_fahrenheit_intentional_failure():
    """
    INTENTIONALLY FAILING TEST.
    Asserts an incorrect Fahrenheit value to demonstrate CI pipeline catching failures.
    FIX: Change 80.0 to 72.5 to make this test pass.
    """
    result = celsius_to_fahrenheit(22.5)
    assert result == 39.0  


def test_weather_description_intentional_failure():
    """
    INTENTIONALLY FAILING TEST.
    Asserts an incorrect description for weather code 0.
    FIX: Change "Sunny" to "Clear sky" to make this test pass.
    """
    description = get_weather_description(0)
    assert description == "Warm"  



def test_classify_temperature_intentional_failure():
    """
    INTENTIONALLY FAILING TEST.
    Asserts an incorrect category for 25°C.
    FIX: Change "Cold" to "Warm" to make this test pass.
    """
    result = classify_temperature(25)
    assert result == "freezing"  