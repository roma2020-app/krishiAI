from google.genai import types

from krishi_ai.adk_service import (
    runner,
    USER_ID,
    SESSION_ID,
)


def ask_adk(question: str):

    content = types.Content(
        role="user",
        parts=[
            types.Part(text=question)
        ],
    )

    response_text = ""

    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content,
    ):

        if event.is_final_response():

            if event.content:

                response_text = event.content.parts[0].text

    return response_text