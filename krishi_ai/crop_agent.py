from google.adk.agents.llm_agent import Agent
from tools.crop_tool import recommend_crop

def crop_tool(village: str, soil: str, rainfall: int):
    return recommend_crop(village, soil, rainfall)

crop_agent = Agent(
    name="crop_agent",
    model="gemini-2.5-flash",
    description="Recommends the best crop for a farmer.",
    instruction="""
You are an agricultural expert.

Use the crop tool to recommend crops.

Always explain:
- Best crop
- Why
- Water requirement
- Expected yield
""",
    tools=[crop_tool],
)