from agents import Agent, Runner, set_default_openai_key
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get("OPENAI_API_KEY")

if not API_KEY:
    raise KeyError("OPENAI_API_KEY environment variable not set.")


# This is only necessary if the OPENAI_API_KEY environment variable is not already set.
set_default_openai_key(key=API_KEY, use_for_tracing=False)


agent = Agent(
    name = "Assistant",
    instructions = "You are a helpful assistant.",
    model = "gpt-4o-mini"
)

result = Runner.run_sync(
    agent,
    "Hello!"
)
print(result.final_output)