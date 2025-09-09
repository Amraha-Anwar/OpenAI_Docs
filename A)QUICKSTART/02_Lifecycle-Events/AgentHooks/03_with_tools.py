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


start_agent = Agent(
    name="Main Agent",
    instructions="You are a helper Agent. Help user with their query. If user ask to generate random number, use tool [random_number] and show the final result.",
    tools = [random_number],
    hooks=CustomAgentHooks(agent_name="Main Agent"),
    model=model

)


async def main():
    await Runner.run(
        start_agent,
        input=f"Generate a random number between 0 and 50",
    )

    print("Done!")


asyncio.run(main())


# OUTPUT👇🏻

# Main Agent 1:
# Main Agent Started!
# Main Agent 2:
# Main Agent started tool random_number
# Main Agent 3:
# Main Agent ended tool random_number with result 34
# Main Agent 4:
# Main Agent Ended with output:
# A random number between 0 and 50 is 34.
# Done!