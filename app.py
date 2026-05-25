import requests

API_BASE_URL = "https://api.open-meteo.com/v1/forecast"

def get_weather(latitude: float, longitude: float) -> dict:
    """
    Fetch current weather data from Open-Meteo API.
    No API key required.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "hourly": "relative_humidity_2m"
    }
    response = requests.get(API_BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_temperature(weather_data: dict) -> float:
    """Extract current temperature in Celsius from API response."""
    return weather_data["current_weather"]["temperature"]


def get_wind_speed(weather_data: dict) -> float:
    """Extract current wind speed in km/h from API response."""
    return weather_data["current_weather"]["windspeed"]


def get_weather_description(weather_code: int) -> str:
    """
    Convert WMO weather code to human-readable description.
    Full code list: https://open-meteo.com/en/docs
    """
    code_map = {
        0:  "Clear sky",
        1:  "Mainly clear",
        2:  "Partly cloudy",
        3:  "Overcast",
        45: "Fog",
        48: "Icy fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Slight showers",
        81: "Moderate showers",
        82: "Violent showers",
        95: "Thunderstorm",
    }
    return code_map.get(weather_code, "Unknown condition")


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius temperature to Fahrenheit."""
    return round((celsius * 9 / 5) + 32, 2)


def is_strong_wind(wind_speed_kmh: float) -> bool:
    """Return True if wind speed exceeds 50 km/h (strong wind threshold)."""
    return wind_speed_kmh > 50


def classify_temperature(celsius: float) -> str:
    """Classify temperature into a human-readable category."""
    if celsius < 0:
        return "Freezing"
    elif celsius < 10:
        return "Cold"
    elif celsius < 20:
        return "Mild"
    elif celsius < 30:
        return "Warm"
    else:
        return "Hot"


if __name__ == "__main__":
    # Example: Get weather for Box Hill, Melbourne (latitude: -37.8823, longitude: 145.1228)
    weather = get_weather(latitude=-37.8823, longitude=145.1228)
    temp = get_temperature(weather)
    wind = get_wind_speed(weather)
    weather_code = weather["current_weather"]["weathercode"]
    description = get_weather_description(weather_code)
    
    print(f"Temperature: {temp}°C ({celsius_to_fahrenheit(temp)}°F)")
    print(f"Wind Speed: {wind} km/h")
    print(f"Condition: {description}")
    print(f"Classification: {classify_temperature(temp)}")