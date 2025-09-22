from agents import Agent, Runner, function_tool, FunctionTool
from dotenv import load_dotenv

load_dotenv()


@function_tool(docstring_style="numpy", name_override="add", description_override = "this is a description" ,use_docstring_info = False)
def add_in_numpy(a: int, b: int) -> int:
    """return the sum of two numbers

    a : int
        The first number.
    b : int
        The second number.
    """
    return a + b

agent = Agent(
    name="Mathematician", 
    instructions="You are math expert", 
    model='gpt-4o-mini', 
    tools=[add_in_numpy],
)
result = Runner.run_sync(starting_agent=agent, input="What is 2+2")
print(result.final_output)
for tool in agent.tools:
    if isinstance(tool, FunctionTool):
        print(f"Tool name: {tool.name}")
        print(f"Tool Description: {tool.description}")
        print(f"Is enabled: {tool.is_enabled}")
        print()

# OUTPUT 👇🏻

# The sum of 2 + 2 is 4.
# Tool name: add
# Tool Description:  ----empty cuz we restrict it to use the docstring description
# Is enabled: True

# --------------

# \( 2 + 2 = 4 \)
# Tool name: add
# Tool Description: this is a description  (now it will use this overridden description even set to False)
# Is enabled: True
