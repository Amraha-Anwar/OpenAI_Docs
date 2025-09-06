from agents import Agent, Runner, function_tool
from agents.agent import StopAtTools
from dotenv import load_dotenv
from typing import Literal
from rich import print
import asyncio, os

load_dotenv()

@function_tool
def divide(a: int, b:int)-> int:
    """
    Returns the division of two numbers

    Args:
        a: first number
        b: second number
    """
    return a // b

@function_tool
def multiply(a: int, b:int)-> int:
    """
    Returns the multiplication of two numbers

    Args:
        a: first number
        b: second number
    """
    return a * b

async def main():
    agent = Agent(
        name = "Math Expert",
        instructions = "You are math expert",
        model = 'gpt-4o-mini',
        tools = [multiply, divide],
        tool_use_behavior = "stop_on_first_tool"
                    # StopAtTools(
            # stop_at_tool_names = ["divide"]
                    # )
    )

    result = await Runner.run(
        agent,
        "What is multiplication of 2 and 5? and What is the division of 5 and 2?"
    )

    print(result.final_output)

asyncio.run(main())

# OUTPUT 👇🏻 (by setting tool='multiply' as stop_at_tool_names)
# 10

# OUTPUT 👇🏻 (by setting tool='divide' as stop_at_tool_names)
# 2