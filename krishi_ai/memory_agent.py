from google.adk.agents.llm_agent import Agent
from krishi_ai.tools.profile_tool import save_profile, load_profile

memory_agent = Agent(
    name="memory_agent",
    model="gemini-2.5-flash",
    description="Stores and retrieves farmer profile information.",
    instruction="""
You manage farmer memory.

If the user provides:
- village
- crop
- soil

call save_profile().

If user asks anything about farming,
first call load_profile().

If no profile exists,
ask the farmer politely.
""",
    tools=[
        save_profile,
        load_profile,
    ],
)