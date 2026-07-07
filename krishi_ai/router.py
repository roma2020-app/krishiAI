import re

from tools.crop_tool import recommend_crop
from tools.weather_tool import get_weather
from tools.profile_tool import save_profile, load_profile
from tools.vision_tool import analyze_leaf
from tools.ticket_tool import create_ticket
from tools.scheme_tool import government_scheme
from tools.market_tool import market_price
from tools.location_tool import extract_location


class IntelligentRouter:

    def route(self, query: str, user_id="farmer1"):

        q = query.lower()

        # -----------------------------
        # Load Farmer Profile
        # -----------------------------

        profile = load_profile(user_id)

        village = None
        crop = "Soybean"

        if isinstance(profile, dict):

            village = profile.get("Village")

            crop = profile.get("Crop", crop)

        # ------------------------------------
        # WEATHER
        # ------------------------------------

        if any(word in q for word in [
            "weather",
            "rain",
            "rainfall",
            "temperature",
            "humidity",
            "forecast",
            "wind",
            "irrigation"
        ]):

            # First try to extract city from question
            detected_location = extract_location(query)

            if detected_location:
                village = detected_location

            # If still not found, use profile
            if not village:
                village = "Nashik"

            return {
                "route": "weather",
                "result": get_weather(village)
            }

        # ------------------------------------
        # CROP
        # ------------------------------------

        if any(word in q for word in [
            "crop",
            "grow",
            "cultivate",
            "recommend"
        ]):

            return {
                "route": "crop",
                "result": recommend_crop(query)
            }

        # ------------------------------------
        # MARKET
        # ------------------------------------

        if any(word in q for word in [
            "price",
            "market",
            "mandi",
            "rate"
        ]):

            return {
                "route": "market",
                "result": market_price(crop)
            }

        # ------------------------------------
        # GOVERNMENT
        # ------------------------------------

        if any(word in q for word in [
            "scheme",
            "subsidy",
            "government",
            "insurance",
            "pm-kisan"
        ]):

            return {
                "route": "scheme",
                "result": government_scheme(query)
            }

        # ------------------------------------
        # DISEASE
        # ------------------------------------

        if any(word in q for word in [
            "image",
            "photo",
            "leaf",
            "disease",
            "yellow",
            "spot",
            "fungus"
        ]):

            return {
                "route": "vision"
            }

        # ------------------------------------
        # SAVE PROFILE
        # ------------------------------------

        if any(word in q for word in [
            "my village",
            "my crop",
            "my soil"
        ]):

            save_profile(user_id, query)

            return {
                "route": "profile",
                "result": "Farmer profile saved successfully."
            }

        # ------------------------------------
        # DEFAULT
        # ------------------------------------

        return {
            "route": "llm"
        }