from typing import Any
from agents import Agent, Runner, RunContextWrapper, FunctionTool
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

def do_some_work(data:str) -> str:
    return "Done"

class FuncArgs(BaseModel):
    username: str
    age: int


async def run_function(ctx: RunContextWrapper[Any], arg:str) -> str:
    parsed = FuncArgs.model_validate_json(arg)
    return do_some_work(data=f"{parsed.username} is {parsed.age} years old")

tool = FunctionTool(
    name = "process_user",
    description = "Processes Exctracted User data",
    params_json_schema = FuncArgs.model_json_schema(),
    on_invoke_tool = run_function
)

agent = Agent(
    name="Processor",
    instructions="You are an assistant that processes user's data using tools when appropriate.",
    tools=[tool],
    model = 'gpt-4o-mini'
)


result = Runner.run_sync(
    agent,
    "The user's name is lica and she is 15 years old."
)

print(result.final_output)



# OUTPUT 👇🏻

# The information for the user Lica has been processed. If you need anything else, feel free to ask!