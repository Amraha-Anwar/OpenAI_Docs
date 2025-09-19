from agents import Agent, Runner, function_tool, FunctionTool
from dotenv import load_dotenv
import asyncio, json
from rich import print
import random

load_dotenv()

@function_tool(name_override="number_picker")  # now this function's name is 'number_picker' instead of 'random_number'
def random_number()->str:
    """generate and returns random number"""
    num = random.randint(1, 10)
    return f"My randomly generated number is ⭐ {num} ⭐"

agent = Agent(
    name = "Assistant",
    instructions = "You are helpful Assistant. Help user with their query"
    "If user ask for a random number, you must have to use the tool [random_number] and give them response consicely.",
    tools = [random_number],
    model = 'gpt-4o-mini' 
)

for tool in agent.tools:
    if isinstance(tool, FunctionTool):
        print(f"Tool Name: {tool.name}")
        print(f"Tool Description: {tool.description}")
        print(f"JSON Schema:\n{json.dumps(tool.params_json_schema, indent=2 )}")
        print()


async def main():
    response = await Runner.run(
        agent,
        "I want you to pick a random number for me"
    )

    print(f"Final Output: {response.final_output}")

asyncio.run(main())



# OUTPUT 👇🏻

# Tool Name: number_picker
# Tool Description: generate and returns random number
# JSON Schema:
# {
#   "properties": {},
#   "title": "number_picker_args",
#   "type": "object",
#   "additionalProperties": false,
#   "required": []
# }

# Final Output: The random number I picked is ⭐ 10 ⭐.