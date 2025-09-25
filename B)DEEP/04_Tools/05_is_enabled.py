from agents import Agent, Runner, function_tool, RunContextWrapper
from dotenv import load_dotenv

load_dotenv()

async def enabled_func(ctx: RunContextWrapper, agent: Agent)-> bool:
    return True

@function_tool(is_enabled = enabled_func)
def add(a: int, b: int) -> int:
    """return the sum of two numbers

    a : int
        The first number.
    b : int
        The second number.
    """
    return a + b

agent = Agent(
    name="Mathematician", 
    instructions="You are math expert. If user asks you to sum any number you must have to use the tool [add]"
    "If tool is not available, do apology and Don't reply by yourself.", 
    model='gpt-4o-mini', 
    tools=[add],
)
result = Runner.run_sync(starting_agent=agent, input="What is 2+2")
print(result.final_output)