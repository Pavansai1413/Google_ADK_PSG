# main.py
import asyncio
import uuid
import json
from typing import Any, Generator

from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai.types import Content

from Interview_simulator.router_agent import router_agent

load_dotenv()

APP_NAME = "interview-simulator"
USER_ID = "pavan-local"

async def run_conversation():
    print("Interview Simulator started")
    print("Type 'exit' to quit.\n")

    session_id = str(uuid.uuid4())
    runner = InMemoryRunner(
        app_name=APP_NAME,
        agent=router_agent,
    )
    runner_session_service = (
        getattr(runner, "session_service", None)
        or getattr(runner, "_session_service", None)
    )
    if runner_session_service is None:
        raise RuntimeError("Could not access runner's session service (session_service/_session_service missing).")

    session = await runner_session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )

    sid = getattr(session, "session_id", None) or getattr(session, "id", None) or session_id
    print(f"Session created: {sid}\n")

    while True:
        user_input = input("User: ").strip()
        if user_input.lower() in ("exit", "quit", "q"):
            print("\nGoodbye!")
            break
        if not user_input:
            continue

        print("\nProcessing...\n")

        new_message = Content(parts=[{"text": user_input}])

        events: Generator[Any, None, None] = runner.run(
            user_id=USER_ID,
            session_id=sid,
            new_message=new_message,
        )

        captured_state = {}
        print("Aqua: ", end="", flush=True)

        for event in events:
            content = getattr(event, "content", None)
            parts = getattr(content, "parts", None) if content else None
            if parts:
                for part in parts:
                    chunk = part.get("text") if isinstance(part, dict) else getattr(part, "text", None)
                    if chunk:
                        print(chunk, end="", flush=True)

            state = getattr(event, "state", None)
            if isinstance(state, dict):
                captured_state.update(state)

        print("\n")

        if captured_state:
            print("Captured outputs:")
            for k, v in captured_state.items():
                if v and not str(k).startswith("_"):
                    preview = str(v)[:600] + ("..." if len(str(v)) > 600 else "")
                    print(f"• {k}:\n{preview}\n")

        print("-" * 80 + "\n")

if __name__ == "__main__":
    asyncio.run(run_conversation())
