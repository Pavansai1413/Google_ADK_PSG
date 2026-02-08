from google.adk.agents import LlmAgent
from vertexai.generative_models import HarmBlockThreshold, HarmCategory, SafetySetting

from google.adk import Agent
from google.adk.tools import google_search
from Interview_simulator.tools.parse_tool import parse_document_tool

from . import prompt

MODEL = "gemini-2.5-pro"


analyzer_agent = Agent(
    model=MODEL,
    name="analyzer_agent",
    instruction=prompt.ANALYZER_PROMPT,
    output_key="analyzer_output",
    tools=[parse_document_tool]
)