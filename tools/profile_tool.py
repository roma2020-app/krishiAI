import re
from .memory_tool import save_farmer, get_farmer

def save_profile(user_id: str, text: str):
    """
    Extract village, crop and soil from user message and save.
    """

    village = None
    crop = None
    soil = None

    villages = [
        "nashik","pune","nagpur",
        "kolhapur","satara","aurangabad"
    ]

    crops = [
        "soybean","cotton","rice",
        "wheat","tomato","millet"
    ]

    soils = [
        "black","red","sandy","clay"
    ]

    lower = text.lower()

    for v in villages:
        if v in lower:
            village = v.title()

    for c in crops:
        if c in lower:
            crop = c.title()

    for s in soils:
        if s in lower:
            soil = s.title()

    if village or crop or soil:
        save_farmer(
            user_id,
            village,
            crop,
            soil
        )

    return "Profile Updated"


def load_profile(user_id: str):

    data = get_farmer(user_id)

    if not data:
        return "No farmer profile found."

    return {
        "Village": data[0],
        "Crop": data[1],
        "Soil": data[2]
    }