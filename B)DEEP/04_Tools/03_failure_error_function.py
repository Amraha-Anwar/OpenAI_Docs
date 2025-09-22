from agents import Agent, Runner, function_tool, RunContextWrapper
from dotenv import load_dotenv
import asyncio

load_dotenv()


def custom_error_function(ctx: RunContextWrapper, error: Exception) -> str:
    print(f"Oops! Something went wrong while calling the tool:\n\n{error}")
    return "Internal Server Error. Can't call tool"


@function_tool(failure_error_function = custom_error_function)
def sum(a: int, b: int) -> str:
    """returns the sum of 2 integers
    
    Args:
        a: number 1
        b: number 2
    """
    raise ValueError("!Error while Calling tool!")


agent = Agent(
    name = "Mathematician",
    instructions = "You are a mathematician. use tool [sum] for addition tasks. Don't answer by yourself",
    model = 'gpt-4o-mini',
    tools = [sum]
)

result = Runner.run_sync(
    agent,
    "what is the sum of 5 and 2?"
)

print(result.final_output)


# OUTPUT 👇🏻
# Oops! Something went wrong while calling the tool:

# !Error while Calling tool!
# It seems there's a temporary issue with the tool. Please try again later!