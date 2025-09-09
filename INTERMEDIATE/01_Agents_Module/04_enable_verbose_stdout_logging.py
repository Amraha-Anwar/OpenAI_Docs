from agents import Agent, Runner, enable_verbose_stdout_logging
from dotenv import load_dotenv
import os

load_dotenv()
enable_verbose_stdout_logging()

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