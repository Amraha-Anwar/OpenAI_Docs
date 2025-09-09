from agents import Agent, function_tool
from dotenv import load_dotenv
import asyncio

load_dotenv()


class OutputType:
    output: str

@function_tool
def what_is_your_name() -> str:
    """Returns the name of the agent."""
    return "Agent007"


agent = Agent(
    name="ToolUserAgent",
    instructions = "Use the tool to get my name.",
    tools=[what_is_your_name],
    model = 'gpt-4o-mini',
)

async def main():
    get_tools = await agent.get_all_tools(run_context=OutputType)
    print(get_tools)

asyncio.run(main())


# OUTPUT 👇🏻

# [FunctionTool(name='what_is_your_name', description='Returns the name of the agent.', params_json_schema={'properties': {}, 'title': 'what_is_your_name_args', 'type': 'object', 'additionalProperties': False, 'required': []}, on_invoke_tool=<function function_tool.<locals>._create_function_tool.<locals>._on_invoke_tool at 0x0000017F33C8BE20>, strict_json_schema=True, is_enabled=True)]