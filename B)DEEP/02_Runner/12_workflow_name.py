from agents import Agent, Runner, RunConfig
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    name= "Assistant Agent",
    instructions = "Help user with their query",
    model= "gpt-4o-mini"
)

result = Runner.run_sync(
    starting_agent = agent,
    input = "Breakdown 5 top specialities of Pakistani culture.",
    run_config = RunConfig(
        workflow_name = "Tracing Workflow"
    )
)

print(result.final_output)

# NOTE 📌

# Workflow Name has changed from "Agent Workflow" to "Tracing Workflow" in tracing