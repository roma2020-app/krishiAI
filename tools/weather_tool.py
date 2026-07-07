from geopy.geocoders import Nominatim
import requests

weather_cache = {}

geolocator = Nominatim(user_agent="krishi_ai")


def get_weather(village):

    if village in weather_cache:
        return weather_cache[village]

    location = geolocator.geocode(village)

    if not location:

        return {
            "village": village,
            "temperature": "N/A",
            "humidity": "N/A",
            "rain_probability": "N/A",
            "wind": "N/A",
            "advice": "Location not found."
        }

    lat = location.latitude
    lon = location.longitude

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
        "&hourly=precipitation_probability"
    )

    data = requests.get(url).json()

    temperature = data["current"]["temperature_2m"]
    humidity = data["current"]["relative_humidity_2m"]
    wind = data["current"]["wind_speed_10m"]
    rain = data["hourly"]["precipitation_probability"][0]

    if rain > 70:
        advice = "Heavy rain expected. Avoid irrigation."

    elif rain > 40:
        advice = "Light rain expected. Irrigate only if soil is dry."

    else:
        advice = "No rain expected. Irrigation recommended."

    result = {
        "village": village.title(),
        "temperature": temperature,
        "humidity": humidity,
        "rain_probability": rain,
        "wind": wind,
        "advice": advice,
    }

    weather_cache[village] = result

    return result


def get_hourly_forecast(village):
    """
    Get 24-hour temperature forecast for a village.
    """
    location = geolocator.geocode(village)
    if not location:
        return None

    lat = location.latitude
    lon = location.longitude

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        "&hourly=temperature_2m"
    )

    try:
        data = requests.get(url).json()
        times = data["hourly"]["time"][:24]
        temps = data["hourly"]["temperature_2m"][:24]
        # Format times to look nice (e.g. 09:00)
        formatted_times = [t.split("T")[1][:5] for t in times]
        return {
            "times": formatted_times,
            "temperatures": temps
        }
    except Exception:
        return None
from geopy.geocoders import Nominatim
import requests

weather_cache = {}

geolocator = Nominatim(user_agent="krishi_ai")


def get_weather(village):

    if village in weather_cache:
        return weather_cache[village]

    location = geolocator.geocode(village)

    if not location:

        return {
            "village": village,
            "temperature": "N/A",
            "humidity": "N/A",
            "rain_probability": "N/A",
            "wind": "N/A",
            "advice": "Location not found."
        }

    lat = location.latitude
    lon = location.longitude

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
        "&hourly=precipitation_probability"
    )

    data = requests.get(url).json()

    temperature = data["current"]["temperature_2m"]
    humidity = data["current"]["relative_humidity_2m"]
    wind = data["current"]["wind_speed_10m"]
    rain = data["hourly"]["precipitation_probability"][0]

    if rain > 70:
        advice = "Heavy rain expected. Avoid irrigation."

    elif rain > 40:
        advice = "Light rain expected. Irrigate only if soil is dry."

    else:
        advice = "No rain expected. Irrigation recommended."

    result = {
        "village": village.title(),
        "temperature": temperature,
        "humidity": humidity,
        "rain_probability": rain,
        "wind": wind,
        "advice": advice,
    }

    weather_cache[village] = result

    return result


def get_hourly_forecast(village):
    """
    Get 24-hour temperature forecast for a village.
    """
    location = geolocator.geocode(village)
    if not location:
        return None

    lat = location.latitude
    lon = location.longitude

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        "&hourly=temperature_2m"
    )

    try:
        data = requests.get(url).json()
        times = data["hourly"]["time"][:24]
        temps = data["hourly"]["temperature_2m"][:24]
        # Format times to look nice (e.g. 09:00)
        formatted_times = [t.split("T")[1][:5] for t in times]
        return {
            "times": formatted_times,
            "temperatures": temps
        }
    except Exception:
        return None
