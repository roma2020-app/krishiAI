from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="krishi_ai")


def extract_location(query):

    words = query.replace("?", "").split()

    ignore = {
        "weather",
        "rain",
        "forecast",
        "temperature",
        "humidity",
        "today",
        "tomorrow",
        "in",
        "of",
        "for",
        "what",
        "is",
        "the",
        "should",
        "i",
        "my",
        "farm"
    }

    candidates = []

    for word in words:
        if word.lower() not in ignore:
            candidates.append(word)

    for word in candidates:

        try:

            location = geolocator.geocode(
                word + ", India",
                timeout=5
            )

            if location:
                return word.title()

        except:
            pass

    return None