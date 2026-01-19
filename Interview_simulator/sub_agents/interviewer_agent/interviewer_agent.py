from google.adk import Agent
from google.adk.tools import google_search
from . import prompt

MODEL = "gemini-2.5-pro"

interviewer_agent = Agent(
    model=MODEL,
    name="interviewer_agent",
    instruction=prompt.INTERVIEWER_PROMPT,
    output_key="interviewer_output",
    tools=[google_search]
)