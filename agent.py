from google.adk.agents.llm_agent import Agent

# Crop
from tools.crop_tool import recommend_crop

# Weather
from tools.weather_tool import get_weather

# Memory
from tools.profile_tool import (
    save_profile,
    load_profile,
)

# Vision
from tools.vision_tool import analyze_leaf

# Ticket
from tools.ticket_tool import create_ticket

# Government Schemes
from tools.scheme_tool import government_scheme

# Market
from tools.market_tool import market_price


root_agent = Agent(
    name="krishi_ai",
    model="gemini-2.5-flash",
    description="AI Agriculture Intelligence Platform",

    instruction="""
You are Krishi AI.

You are an intelligent agricultural assistant.

IMPORTANT RULES

1. Never guess if a tool can answer.

2. Before crop or weather advice,
   first call load_profile().

3. If no farmer profile exists,
   politely ask for:
   - Village
   - Soil Type
   - Crop (if already planted)

4. When the user provides profile information,
   call save_profile().

5. If the user asks:
   - crop recommendation
       -> recommend_crop()

   - weather / irrigation / rainfall
       -> get_weather()

   - uploads a crop image
       -> analyze_leaf()

   - government schemes
       -> government_scheme()

   - market prices
       -> market_price()

   - expert help
       -> create_ticket()

6. Call ONLY the minimum number of tools needed.

7. Keep answers short and farmer-friendly.

8. Use previous farmer profile whenever possible.

9. If disease confidence is low,
   recommend expert support and create a ticket.

10. Never call Vision unless an image is provided.
""",

    tools=[
        load_profile,
        save_profile,
        recommend_crop,
        get_weather,
        analyze_leaf,
        government_scheme,
        market_price,
        create_ticket,
    ],
)