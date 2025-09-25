from agents import Agent, Runner, function_tool, RunContextWrapper
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class MyContext(BaseModel):
    user_input: str

async def enabled_func(ctx: RunContextWrapper[MyContext], agent: Agent) -> bool:
    if ctx.context.user_input == "What is 2+2":
        return True
    else:
        print("I'm sorry! The tool is disabled at the backend")
        return False

@function_tool(is_enabled=enabled_func)
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
    instructions="You are a math expert. If the user asks you to sum any numbers, you must use the [add] tool. "
    "If the tool is not available, apologize and do not reply by yourself.",
    model='gpt-4o-mini',
    tools=[add],
)

my_context = MyContext(user_input="What is 2+2")

result = Runner.run_sync(starting_agent=agent, input=my_context.user_input, context=my_context)
print(result.final_output)


# OUTPUT 👇🏻

# I'm sorry! The tool is disabbled at the backend
# I apologize, but I'm unable to calculate that right now.