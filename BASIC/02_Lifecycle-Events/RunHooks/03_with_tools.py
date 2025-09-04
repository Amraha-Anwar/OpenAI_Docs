from agents import (
    Agent,
    Runner, 
    AsyncOpenAI, 
    OpenAIChatCompletionsModel, 
    RunContextWrapper, 
    RunHooks, 
    set_tracing_disabled,
    Tool,
    function_tool
)
from dotenv import load_dotenv
import random
import asyncio
import os

load_dotenv()
set_tracing_disabled(True)

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

class TestRunHook(RunHooks):
    def __init__(self):
        self.event_counter = 0
        self.name = "Test Hook"

    async def on_agent_start(self, context:RunContextWrapper, agent:Agent )->None:
        self.event_counter += 1
        print(f"{self.name} {self.event_counter}:\n{agent.name} Started!\nUsage:{context.usage}\n")

    async def on_agent_end(self, context:RunContextWrapper, agent:Agent, output:any)-> None:
        self.event_counter += 1
        print(f"{self.name} {self.event_counter}:\n{agent.name} Ended!\nUsage:{context.usage}\nOUTPUT:\n\n{output}\n")

    async def on_tool_start(self, context:RunContextWrapper, agent:Agent, tool:Tool) -> None:
        self.event_counter += 1
        print(f"{self.name} {self.event_counter}:\n{tool.name} Tool Started\nUsage: {context.usage}\n")

    async def on_tool_end(self, context:RunContextWrapper, agent:Agent, tool:Tool, result: str)-> None:
        self.event_counter += 1
        print(f"{self.name} {self.event_counter}:\n{tool.name} Tool Ended with result: {result} \nUsage: {context.usage}\n")

@function_tool
def random_number(max: int) -> int:
    """
    Generate a random number upto the provided maximum.
    """
    return random.randint(0, max)


main_agent = Agent(
    name="Main Agent",
    instructions="You are a helper Agent. Help user with their query. If user ask to generate random number, use tool [random_number] and show the final result.",
    tools = [random_number],
    model=model
)

async def main() -> None:
    user_input = input("Enter a max number: ")
    await Runner.run(
        main_agent,
        hooks=TestRunHook(),
        input=f"Generate a random number between 0 and {user_input}.",
    )

asyncio.run(main())


# OUTPUT 👇🏻

# Enter a max number: 23
# Test Hook 1:
# Main Agent Started!
# Usage:Usage(requests=0, input_tokens=0, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=0, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=0)

# Test Hook 2:
# random_number Tool Started
# Usage: Usage(requests=1, input_tokens=88, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=16, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=176)

# Test Hook 3:
# random_number Tool Ended with result: 19 
# Usage: Usage(requests=1, input_tokens=88, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=16, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=176)

# Test Hook 4:
# Main Agent Ended!
# Usage:Usage(requests=2, input_tokens=209, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=24, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=305)
# OUTPUT:

# The random number is 19.