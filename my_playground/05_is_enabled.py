from agents import Agent, Runner, ModelSettings, function_tool
from dotenv import load_dotenv
import random

load_dotenv()

@function_tool(is_enabled = False)
def random_number(num1: int, num2: int)-> str:
    """generates random number
    
    Arg
        num1: the frst number from which the limit starts
        num2: the last limit number 
    """
    return f"The random number I've chosen for you is 🔢{random.randint(num1, num2)}🔢"

agent = Agent(
    name = "number generator",
    instructions = "you are a mathematician. If user asks you to choose any random number, you must have to use the tool"
    "If the tool is not available, do apologies but Don't respond by yourself.",
    model = 'gpt-4o-mini',
    tools = [random_number],
    model_settings = ModelSettings(
        tool_choice = 'required'
    )
)

response = Runner.run_sync(
    agent,
    "I'm confused, choose a random number for me between 1 - 10."
)

print(response.final_output)


# OUTPUT 👇🏻 (is_enabled = False, tool_choice = "required")
# openai.BadRequestError: Error code: 400


# OUTPUT 👇🏻 (is_enabled = True, tool_choice = 'none)
# I'm unable to select a random number at the moment. Please try again later!