import os
import uvicorn
import asyncio
import uuid
import json
import shutil
import logging
from fastapi import FastAPI, Body, UploadFile, File
from typing import Any, Generator, Dict
from dotenv import load_dotenv

from google.adk.runners import InMemoryRunner
from google.genai.types import Content, Part
from google.adk.cli.fast_api import get_fast_api_app

from Interview_simulator.router_agent import router_agent

load_dotenv()



APP_NAME = "interview-simulator"
USER_ID = "pavan-local"

# Agent directory
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Initializing Session DB
SESSION_SERVICE_URI = "sqlite+aiosqlite:///./session.db"

# Initializing CORS
ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
    "*"
]

SERVE_WEB_INTERFACE = True

app: FastAPI = get_fast_api_app(
    agents_dir = AGENT_DIR,
    session_service_uri = SESSION_SERVICE_URI,
    allow_origins = ALLOWED_ORIGINS,
    web=SERVE_WEB_INTERFACE,
    trace_to_cloud=True
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/chat")
async def chat(body: Dict[str, Any] = Body(...)):
    user_input = body.get("message")
    if not user_input:
        return {"error": "No message provided" }
    session_id = body.get("session_id", str(uuid.uuid4()))
    logger.info(f"Processing message for session {session_id}: {user_input[:50]}...")

    runner = InMemoryRunner(
        app_name=APP_NAME,
        agent=router_agent
    )

    session_service = getattr(runner, "session_service", None)
    if not session_service:
        raise RuntimeError("Session service not found in runner")
    
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )

    new_message = Content(parts=[Part(text=user_input)])

    events = runner.run(
        user_id=USER_ID,
        session_id=session_id,
        new_message=new_message,
    )

    response_text = ""
    captured_state = {}

    for event in events:
        content = getattr(event, "content", None)
        parts = getattr(content, "parts", None) if content else None
        if parts:
            for part in parts:
                chunk = getattr(part, "text", None)
                if chunk:
                    response_text += chunk

        state = getattr(event,"state", None)
        if isinstance(state, dict):
            captured_state.update(state)

    logger.info(f"Response generated for session {session_id}")
    return {
        "response":response_text,
        "session_id":session_id,
        "captured_state":captured_state
    }


@app.post("/upload")
async def upload_files(
    resume: UploadFile = File(None),
    jd: UploadFile = File(None)):

    paths={}
    if resume:
        resume_path = f"./temp_{resume.filename}"
        with open(resume_path, "wb") as f:
            shutil.copyfileobj(resume.file, f)
        paths["resume"] = resume_path
    if jd:
        jd_path = f"./temp_{jd.filename}"
        with open(jd_path, "wb") as f:
            shutil.copyfileobj(jd.file, f)
        paths["jd"] = jd_path
    return {"paths": paths}


if __name__=='__main__':
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        reload=True
    )
    
