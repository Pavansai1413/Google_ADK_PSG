from vertexai.preview import reasoning_engines
from vertexai import agent_engines
from Interview_simulator.router_agent import router_agent
import os
from dotenv import load_dotenv
import vertexai
import sys

load_dotenv()


def main():
    PROJECT_ID = "vertex-ai-demo-psg"
    LOCATION = "us-central1"
    STAGING_BUCKET = "gs://vertex-ai-demo-psg-interview-agent-artifacts"

    print("Deploy started with project:", PROJECT_ID)

    vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET
    )

    print("Vertex AI initialized")

    adk_app = reasoning_engines.AdkApp(
    agent=router_agent,
    enable_tracing=True,
    )

    print("ADK App created")

    remote_app = agent_engines.create(
    agent_engine=adk_app,
    extra_packages=[ ],
    display_name="Interview-Simulator-Agent",
    requirements=os.path.join(os.path.dirname(__file__), "requirements.txt"),
)

    print("Agent deployed successfully")

if __name__ == "__main__":
    main()
    print("Agent deployed successfully")