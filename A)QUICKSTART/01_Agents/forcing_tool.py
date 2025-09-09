from agents import (Agent, 
                    AsyncOpenAI, 
                    OpenAIChatCompletionsModel, 
                    set_tracing_disabled ,
                    Runner, 
                    function_tool, 
                    ModelSettings,
                    enable_verbose_stdout_logging
                                    )
import os
from dotenv import load_dotenv


load_dotenv()
set_tracing_disabled(disabled = True)
# enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")
url = os.getenv("BASE_URl")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=url,
)

model = OpenAIChatCompletionsModel(
    model = 'gemini-2.0-flash',
    openai_client = external_client,
)


@function_tool
def sum(num1: int, num2: int) -> int:
    """add two numbers.
    
    Args:
        num1 = first number,
        num2 = second number
    """
    return num1 + num2

model_setting = ModelSettings(
    # we have 3 tool choices ('required', 'auto', 'none')
    tool_choice = 'required'
)

starting_agent = Agent(
    name = "Assistant Agent",
    instructions = "Help user with their query",
    model = model,
    tools = [sum],
    model_settings = model_setting
)


result = Runner.run_sync(starting_agent,"add 2301 and 0123")
print(result.final_output)


# OUTPUT 👇🏻
# 2301 + 123 = 2424