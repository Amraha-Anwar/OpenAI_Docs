from agents import Agent
from dotenv import load_dotenv
from rich import print
import asyncio

load_dotenv()


agent = Agent(
    name = "Helpful Assistant",
    instructions = "You are a helpful assistant that provides concise and accurate information.",
    model = "gpt-4o-mini",
)


async def main():
    result = await agent.get_system_prompt("What is the capital of France?")
    print(result)


asyncio.run(main())


# OUTPUT 👇🏻

# You are a helpful assistant that provides concise and accurate information.