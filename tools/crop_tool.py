import pandas as pd

from tools.weather_tool import get_weather

df = pd.read_csv("data/soil.csv")


def recommend_crop(village: str, soil: str,rainfall:int):

    village = village.strip().lower()
    soil = soil.strip().lower()

    weather = get_weather(village)

    result = df[
        (df["Village"].str.lower() == village)
        &
        (df["Soil"].str.lower() == soil)
    ]

    if result.empty:

        return {
            "status": "No Match",
            "message": "No crop found for this village and soil."
        }

    recommendations = []

    for _, row in result.iterrows():

        expected = int(row["Rainfall"])
       #actual = weather["rain_probability"]
        actual = rainfall

        diff = abs(expected - actual)

        confidence = max(50, 100 - diff)

        recommendations.append(
            {
                "crop": row["Crop"],
                "confidence": confidence,
                "groundwater": int(row["Groundwater"]),
                "expected_rainfall": expected
            }
        )

    recommendations.sort(
        key=lambda x: x["confidence"],
        reverse=True
    )

    return {
        "status": "Success",
        "weather": weather,
        "recommendations": recommendations
    }