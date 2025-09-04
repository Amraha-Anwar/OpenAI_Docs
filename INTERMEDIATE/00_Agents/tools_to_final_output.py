from agents import Agent, Runner, function_tool, ModelSettings, FunctionToolResult, RunContextWrapper, ToolCallItem, ToolsToFinalOutputResult
from rich import print
from typing import List
from dotenv import load_dotenv
from dataclasses import dataclass


load_dotenv()

@function_tool
def add_numbers(a: int, b: int) -> int:
    """
    Add two numbers.

    Args:
        a: First number
        b: Second number
    """
    return a + b

async def generate_final_output(ctx: RunContextWrapper[None], result: List[FunctionToolResult]) -> ToolsToFinalOutputResult:
    output=result[0].output
    return ToolsToFinalOutputResult(
        is_final_output=True,
        final_output=250
    )

agent = Agent(
    name="Tools to Final Output",
    instructions = "You are a Maths expert.",
    tools = [add_numbers],
    model = 'gpt-4o-mini',
    tool_use_behavior = generate_final_output,
    model_settings = ModelSettings(
        tool_choice = "required"
    ),
)

result = Runner.run_sync(
    agent,
    "what is the sum of 5432 and 978?"
)
print(result.final_output)


# OUTPUT 👇🏻

# 250       (the output we set in the custom function as 'final-output')