from agents import (
    Agent,
    Runner,
    AgentHooks,
    RunHooks,
    RunContextWrapper,
    function_tool,
    Tool
)
from pydantic import BaseModel
from dotenv import load_dotenv
from rich import print
import asyncio

load_dotenv()

# AgentHooks
class CustomAgentHook(AgentHooks):
    def __init__(self, agent_display_name):
        self.event_count = 0
        self.agent_display_name = agent_display_name

    async def on_start(self, context: RunContextWrapper, agent: Agent) -> None:
        self.event_count += 1
        print(f"\n\t====AGENTHOOKS====\n{self.agent_display_name} {self.event_count}:'{agent.name}' is started!\n")

    async def on_tool_start(self, context:RunContextWrapper,agent: Agent, tool: Tool) -> None:
        self.event_count += 1
        print(f"\t====AGENTHOOKS====\n{self.agent_display_name} {self.event_count}: '{agent.name}' is calling tool '{tool.name}'\n")

    async def on_tool_end(self, context: RunContextWrapper, agent: Agent, tool: Tool, result: str) -> None:
        self.event_count += 1
        print(f"\t====AGENTHOOKS====\n{self.agent_display_name} {self.event_count}: '{agent.name}' has finished calling tool '{tool.name}' with output: {result}\n")

    async def on_handoff(self, context:RunContextWrapper, agent: Agent, source: Agent) -> None:
        self.event_count += 1
        print(f"\t====AGENTHOOKS====\n{self.agent_display_name} {self.event_count}: Handing off from '{source.name}' to '{agent.name}'")

    async def on_end(self, context:RunContextWrapper, agent:Agent, output: any) -> None:
        self.event_count += 1
        print(f"\t====AGENTHOOKS====\n{self.agent_display_name} {self.event_count}: '{agent.name}' has finished with final output: {output}\n")

# RunHooks
class CustomRunHook(RunHooks):
    def __init__(self, run_name):
        self.event_count = 0
        self.run_name = run_name

    async def on_agent_start(self, context:RunContextWrapper, agent:Agent) -> None:
        self.event_count += 1
        print(f"\n\t====RUNHOOKS====\n{self.run_name} {self.event_count}:'{agent.name}' started Run!\n")

    async def on_tool_start(self, context:RunContextWrapper, agent:Agent, tool:Tool) -> None:
        self.event_count += 1
        print(f"\t====RUNHOOKS====\n{self.run_name} {self.event_count}:'{agent.name}' is calling tool '{tool.name}'\n")

    async def on_tool_end(self, context:RunContextWrapper, agent:Agent, tool:Tool, output:any) -> None:
        self.event_count += 1
        print(f"\t====RUNHOOKS====\n{self.run_name} {self.event_count}:'{agent.name}' has finished calling tool '{tool.name}' with output: {output}\n")

    async def on_handoff(self, context:RunContextWrapper, from_agent:Agent, to_agent:Agent) -> None:
        self.event_count += 1
        print(f"\t====RUNHOOKS====\n{self.run_name} {self.event_count}: Handing off from '{from_agent.name}' to '{to_agent.name}'\n")

    async def on_agent_end(self, context:RunContextWrapper, agent:Agent, output:any) -> None:
        self.event_count += 1
        print(f"\t====RUNHOOKS====\n{self.run_name} {self.event_count}:'{agent.name}' ended Run with output: {output}\n")


# Tool
@function_tool
def double_number(number: int) -> str:
    """Doubles the input number.

    Args:
        number (int): The number to double.
    """
    return f"The double of {number} is {number * 2}"


math_agent = Agent(
    name = "MathAgent",
    instructions = "extract the number from user input and double it using the tool [double_number].",
    model = "gpt-4o-mini",
    tools = [double_number],
    hooks = CustomAgentHook(agent_display_name="MathAgent")
)

agent = Agent(
    name="Main Agent",
    instructions="An agent that solves user's queries. If the query is related to doubling a number you must have to handoff to 'math agent'.",
    model="gpt-4o-mini",
    handoffs = [math_agent],
    tools = [double_number],
    hooks = CustomAgentHook(agent_display_name="Main Agent")
)

async def main():
    result = await Runner.run(
        agent,
        input="What is double the number 15?",
        hooks = CustomRunHook(run_name="Running Agent")
    )

    print(f"Final output: {result.final_output}\n")

asyncio.run(main())


# OUTPUT 👇


#         ====RUNHOOKS====
# Running Agent 1:'Main Agent' started Run!

#         ====AGENTHOOKS====
# Main Agent 1:'Main Agent' is started!

#         ====RUNHOOKS====
# Running Agent 2: Handing off from 'Main Agent' to 'MathAgent'

#         ====AGENTHOOKS====
# Main Agent 2: Handing off from 'Main Agent' to 'MathAgent'

#         ====RUNHOOKS====
# Running Agent 3:'MathAgent' started Run!

#         ====AGENTHOOKS====
# MathAgent 1:'MathAgent' is started!

#         ====RUNHOOKS====
# Running Agent 4:'MathAgent' is calling tool 'double_number'

#         ====AGENTHOOKS====
# MathAgent 2: 'MathAgent' is calling tool 'double_number'

#         ====RUNHOOKS====
# Running Agent 5:'MathAgent' has finished calling tool 'double_number' with output: The double of 15 is 30

#         ====AGENTHOOKS====
# MathAgent 3: 'MathAgent' has finished calling tool 'double_number' with output: The double of 15 is 30

#         ====RUNHOOKS====
# Running Agent 6:'MathAgent' ended Run with output: The double of the number 15 is 30.

#         ====AGENTHOOKS====
# MathAgent 4: 'MathAgent' has finished with final output: The double of the number 15 is 30.

# Final output: The double of the number 15 is 30.