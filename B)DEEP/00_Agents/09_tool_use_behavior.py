from agents import (
    Agent,
    Runner,
    function_tool,
    StopAtTools,
    RunContextWrapper,
    FunctionToolResult,
    ToolsToFinalOutputResult,
)
from typing import List
from dotenv import load_dotenv
from rich import print
import asyncio

load_dotenv()

@function_tool
def text_to_uppercase(text: str) -> str:
    """Convert text to uppercase.
    
    Args:
        text (str): The text to convert.
    """
    return text.upper()


@function_tool
def reverse_text(text: str) -> str:
    """Reverse the given text.
    
    Args:
        text (str): The text to reverse.
    """
    return text[::-1]

async def custom_output_function(ctx: RunContextWrapper[None], result: List[FunctionToolResult]) -> ToolsToFinalOutputResult:
    return ToolsToFinalOutputResult(
        is_final_output = True,
        final_output = "This is a custom final output from the tool use behavior."
    )


agent = Agent(
    name = "Assistant",
    instructions= "You are a helpful assistant who helps users with their query."
    "If you need to convert text to uppercase, use the tool [text_to_uppercase]."
    "If you need to reverse text, use the tool [reverse_text].",
    model = 'gpt-4o-mini',
    tools = [text_to_uppercase, reverse_text],
    tool_use_behavior = custom_output_function #custom output function
    # 2: "run_llm_again" (default)
    # 3: "stop_on_first_tool"
    # 4: StopAtTools(
    #     stop_at_tool_names = ["reverse_text"]
    # )
)

async def main():
    result = await Runner.run(
        agent,
        "Convert the text 'hello world' to uppercase. And reverse the word 'Agent'."
    )
    print(result.final_output)

asyncio.run(main())


# OUTPUT 👇🏻 (by setting tool_use_behavior to custom_output_function)
# This is a custom final output from the tool use behavior.


# OUTPUT 👇🏻 (by setting tool='reverse_text' as stop_at_tool_names)
# tnegA


# OUTPUT 👇🏻 (by setting tool='text_to_uppercase' as stop_at_tool_names)
# HELLO WORLD


# OUTPUT 👇🏻 (by setting tool_use_behavior to "stop_on_first_tool")
# HELLO WORLD


# OUTPUT 👇🏻 (by setting tool_use_behavior to "run_llm_again")
# Here are the results you requested:

# - The text 'hello world' in uppercase is: **HELLO WORLD**
# - The word 'Agent' reversed is: **tnegA**
