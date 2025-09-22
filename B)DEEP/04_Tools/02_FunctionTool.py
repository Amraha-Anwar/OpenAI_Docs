from agents import Agent, Runner, FunctionTool, RunContextWrapper
from dotenv import load_dotenv
from typing import Any
from pydantic import BaseModel

load_dotenv()


def tasks(done: str ) -> str:
    return "done"


class Tasks_list(BaseModel):
    grocery : bool
    daily_walk : bool

async def run_func(ctx: RunContextWrapper[Any], arg:str)-> str:
    parsed = Tasks_list.model_validate_json(arg)
    return tasks(done=f"\nGrocery {parsed.grocery} \nDaily Walk: {parsed.daily_walk}")

tool = FunctionTool(
    name = "Todo_checker",
    description = "Checks user's todo list",
    params_json_schema = Tasks_list.model_json_schema(),
    on_invoke_tool = run_func,
    strict_json_schema = True,
    is_enabled = True
)

agent = Agent(
    name = "Helper",
    instructions = "You are an assistant who checks user's todo list if done yet or not by using tool.",
    model = 'gpt-4o-mini',
    tools = [tool]
)


result = Runner.run_sync(
    agent ,
    "I have done the grocery but not walk yet. Update my todo list."
)
print(result.final_output)


# OUTPUT 👇🏻

# Your todo list has been updated! The grocery task is marked as done, 
# but the daily walk is still pending. Let me know if you need anything else!