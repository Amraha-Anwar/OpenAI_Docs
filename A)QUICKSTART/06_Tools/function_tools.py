from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
import asyncio
from rich import print
import random

load_dotenv()

@function_tool
def random_number()->str:
    """generate and returns random number"""
    num = random.randint(1, 10)
    return f"My randomly generated number is ⭐ {num} ⭐"

agent = Agent(
    name = "Assistant",
    instructions = "You are helpful Assistant. Help user with their query"
    "If user ask for a random number, you must have to use the tool [random_number] and give them response consicely.",
    tools = [random_number],
    model = 'gpt-4o-mini' 
)

async def main():
    response = await Runner.run(
        agent,
        "I want you to pick a random number for me",
        max_turns = 1      # will cause "MaxTurnsExceeded Exception" 
    )

    print(response.final_output)

asyncio.run(main())



# OUTPUT 👇🏻

# My randomly generated number is ⭐10⭐