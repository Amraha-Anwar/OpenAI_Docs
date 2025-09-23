from agents import Agent, Runner, function_tool, ModelSettings
from dotenv import load_dotenv
import asyncio

load_dotenv()

@function_tool
def get_weather(city: str)-> str:
    """returns the weather of mentioned city
    
    Args
        city: the city whose weather asked
    """
    return f" the weather of {city} is cloudy."


@function_tool
def doubler(num: int) -> str:
    """returns the double of the given number
    
    Args
        num: number which have to be doubled
    """
    return f"the double of {num} is {num * 2}"

agent = Agent(
    name = "Assistant",
    instructions = "You are a helpful Assistant, help user with their query."
    "If user ask for the weather you must have to use the tool [get_weather]"
    "If user ask to double any number you must have to use the tool [doubler]"
    "Do not respond by yourself.",
    model = 'gpt-4o-mini',
    tools = [get_weather, doubler],
    model_settings = ModelSettings(
        parallel_tool_calls = True
    )
)

async def main():
    result = await Runner.run(
        agent,
        "What is the weather of karachi? also tell me what is the double of 50?"
    )
    print(result.final_output)

asyncio.run(main())