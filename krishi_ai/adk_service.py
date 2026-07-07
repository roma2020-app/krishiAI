import os
from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from krishi_ai.agent import root_agent

load_dotenv()

APP_NAME = "krishi_ai"

USER_ID = "farmer1"
SESSION_ID = "default"

# Session Service
session_service = InMemorySessionService()

# Auto-create the first session
session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
)

# ADK Runner
runner = Runner(
    app_name=APP_NAME,
    agent=root_agent,
    session_service=session_service,
    auto_create_session=True,
)