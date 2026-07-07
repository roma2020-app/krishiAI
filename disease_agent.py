from google.adk.agents.llm_agent import Agent
from krishi_ai.tools.vision_tool import analyze_leaf


def vision_tool(image_path: str):
    return analyze_leaf(image_path)


disease_agent = Agent(
    name="disease_agent",
    model="gemini-2.5-flash",
    description="Diagnose crop diseases from images.",
    instruction="""
Always use the vision tool whenever an image is provided.

Return

Disease

Confidence

Treatment

Prevention
""",
    tools=[vision_tool],
)