from agents import Agent, Runner, set_tracing_disabled
from dotenv import load_dotenv
import os

load_dotenv()
set_tracing_disabled(True)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model = 'gpt-4o-mini',
)

result = Runner.run_sync(
    agent,
    "helloooo"
)

print(result.final_output)