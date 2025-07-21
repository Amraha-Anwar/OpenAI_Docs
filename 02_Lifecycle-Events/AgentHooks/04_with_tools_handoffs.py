from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, RunContextWrapper, AgentHooks, set_tracing_disabled, enable_verbose_stdout_logging, Tool, function_tool
from dotenv import load_dotenv
import asyncio
import random
import os

load_dotenv()
set_tracing_disabled(True)
# enable_verbose_stdout_logging()
gemini_api_key = os.getenv("GEMINI_API_KEY")
url = os.getenv("BASE_URL")
MODEL = 'gemini-2.5-flash'

client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url = url
)

model = OpenAIChatCompletionsModel(
    model = MODEL,
    openai_client = client
)

class CustomAgentHooks(AgentHooks):
    def __init__(self, agent_name: str):
        self.event_counter = 0
        self.agent_name = agent_name

    async def on_start(self, ctx:RunContextWrapper, agent:Agent) -> None:
        self.event_counter += 1
        print(f"{self.agent_name} {self.event_counter}:\n{agent.name} Started!")

    async def on_end(self, ctx:RunContextWrapper, agent: Agent, output: any) -> None:
        self.event_counter += 1
        print(f"{self.agent_name} {self.event_counter}:\n{agent.name} Ended with output:\n{output}")

    async def on_handoff(self, ctx:RunContextWrapper, agent:Agent, source:Agent) -> None:
        self.event_counter += 1
        print(f"{self.agent_name} {self.event_counter}:\n{source.name} handed off to {agent.name}")

    async def on_tool_start(self, ctx:RunContextWrapper, agent:Agent, tool:Tool)-> None:
        self.event_counter += 1
        print(f"{self.agent_name} {self.event_counter}:\n{agent.name} started tool {tool.name}")

    async def on_tool_end(self, ctx:RunContextWrapper, agent:Agent, tool: Tool, result: str)-> None:
        self.event_counter += 1
        print(f"{self.agent_name} {self.event_counter}:\n{agent.name} ended tool {tool.name} with result {result}")

@function_tool
def random_number(max: int) -> int:
    """
    Generate a random number upto the provided maximum.
    """
    return random.randint(0, max)

@function_tool
def multiply_by_two(x: int) -> int:
    """Simple multiplication by two."""
    return x * 2

multiplier_agent = Agent(
    name = "Multiplier Agent",
    instructions = "You are a Multiplier Agent. Multiply the number by 2 and then return the final result.",
    hooks = CustomAgentHooks(agent_name="Multiplier Agent"),
    tools = [multiply_by_two],
    model = model
)

start_agent = Agent(
    name="Main Agent",
    instructions="Generate a random number. If it's even, stop. If it's odd, hand off to the multiplier agent.",
    tools = [random_number],
    handoffs = [multiplier_agent],
    hooks=CustomAgentHooks(agent_name="Main Agent"),
    model=model

)

async def main():
    user_input = input("Enter a max number: ")
    await Runner.run(
        start_agent,
        input=f"Generate a random number between 0 and {user_input}",
    )

    print("Done!")


asyncio.run(main())


# OUTPUT👇🏻

# Enter a max number: 40
# Main Agent 1:
# Main Agent Started!
# Main Agent 2:
# Main Agent started tool random_number
# Main Agent 3:
# Main Agent ended tool random_number with result 22
# Main Agent 4:
# Main Agent Ended with output:
# The number 22 is an even number, so I will stop here.
# Done!

# Main Agent 4:
# Main Agent handed off to Multiplier Agent
# Multiplier Agent 1:
# Multiplier Agent Started!
# Multiplier Agent 2:
# Multiplier Agent started tool multiply_by_two
# Multiplier Agent 3:
# Multiplier Agent ended tool multiply_by_two with result 90
# Multiplier Agent 4:
# Multiplier Agent Ended with output:
# The final result is 90.
# Done!

# Enter a max number: 92
# Main Agent 1:
# Main Agent Started!
# Main Agent 2:
# Main Agent started tool random_number
# Main Agent 3:
# Main Agent ended tool random_number with result 41
# Main Agent 4:
# Main Agent handed off to Multiplier Agent
# Multiplier Agent 1:
# Multiplier Agent Started!
# Multiplier Agent 2:
# Multiplier Agent started tool multiply_by_two
# Multiplier Agent 3:
# Multiplier Agent ended tool multiply_by_two with result 82
# Multiplier Agent 4:
# Multiplier Agent Ended with output:
# The random number generated was 41. When multiplied by 2, the result is 82.

# Done!