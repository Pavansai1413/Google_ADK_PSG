from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from vertexai.generative_models import HarmCategory, HarmBlockThreshold

from .sub_agents.analyzer_agent.analyzer_agent import analyzer_agent
from .sub_agents.interviewer_agent.interviewer_agent import interviewer_agent
from .sub_agents.validation_agent.validation_agent import validation_agent
from . import prompt

MODEL = "gemini-2.5-pro"

router_agent = LlmAgent(
    name="router_agent",
    model=MODEL,
    description=(
        "You are a router agent for an interview simulator workflow. "
        "You are given a user resume and job description and need to route it to the appropriate "
        " series of expert subagents to help the user prepare for the interview."
    ),
    instruction=prompt.router_prompt,
    output_key="router_agent_output",
    tools=[
        AgentTool(agent=analyzer_agent),
        AgentTool(agent=interviewer_agent),
        AgentTool(agent=validation_agent),
    ],
)

root_agent = router_agent