from google.adk import Agent
from . import prompt

MODEL = "gemini-2.5-pro"

validation_agent = Agent(
    model=MODEL,
    name="validation_agent",
    instruction=prompt.VALIDATION_PROMPT,
    output_key="validation_output"
)