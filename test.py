from tools.crop_tool import recommend_crop

print(
    recommend_crop(
        "Nashik",
        "Black",
        800
    )
)

from tools.weather_tool import *

w = get_weather("Nashik")

print(w)

print(irrigation_advice(w))