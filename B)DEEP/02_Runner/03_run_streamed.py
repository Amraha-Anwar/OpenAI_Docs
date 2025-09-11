from agents import (
    Agent,
    Runner,
    RunHooks,
    RunContextWrapper,
    function_tool,
    Tool,
    enable_verbose_stdout_logging
)
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio

load_dotenv()
# enable_verbose_stdout_logging()

class UserInfo(BaseModel):
    name: str
    email: str


@function_tool
def get_user_info(ctx: RunContextWrapper[UserInfo]) -> str:
    """Extract user information from the context."""
    return f"User Name: {ctx.context.name}, Email: {ctx.context.email}"


class CustomRunHook(RunHooks):
    def __init__(self, agent_name):
        self.event_counter = 0
        self.agent_name = agent_name

    async def on_agent_start(self, context: RunContextWrapper, agent:Agent) -> None: 
        self.event_counter += 1
        print(f"{self.agent_name} {self.event_counter}: {agent.name} Started..")

    async def on_tool_start(self, context: RunContextWrapper, agent:Agent, tool:Tool) -> None:
        self.event_counter += 1
        print(f"{self.agent_name} {self.event_counter}: {agent.name} using tool {tool.name}..")

    async def on_tool_end(self, context: RunContextWrapper, agent:Agent, tool:Tool, result: str) -> None:
        self.event_counter += 1
        print(f"{self.agent_name} {self.event_counter}: {agent.name} finished using tool {tool.name} with result: {result}")

    async def on_agent_end(self, context:RunContextWrapper, agent: Agent, output: str) -> None:
        self.event_counter += 1
        print(f"{self.agent_name} {self.event_counter}: {agent.name} Finished with output: {output}")

main_agent = Agent[UserInfo](
    name = "Assistant Agent",
    instructions = "You are a helpful assistant. Provide user information when requested. If you need to process user data, use the get_user_info tool.",
    tools = [get_user_info],
    model = 'gpt-4o-mini',
)

async def main():
    result = Runner.run_streamed(
        starting_agent = main_agent,
        input = "What do you know about me?",
        max_turns = 5,
        hooks = CustomRunHook("Running Main Agent"),
        context = UserInfo(name= "Amraha", email = "amraha@gmail.com")
        )
    async for event in result.stream_events():
        if event.type == "raw_response_event":
            continue
        elif event.type == "agent_updated_stream_event":
            print(f"\nAgent Updated Event: {event.new_agent.name}")
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("Tool was called...")
            elif event.item.type == "tool_call_output_item":
                print(f"\nTool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"\nMessage Output:\n '{event.item.raw_item.content[0].text}'")
            else:
                pass
    
    print("\nFinal Result:", result.final_output)

asyncio.run(main())

# OUTPUT 👇🏻

# Agent Updated Event: Assistant Agent
# Running Main Agent 1: Assistant Agent Started..
# Tool was called...
# Running Main Agent 2: Assistant Agent using tool get_user_info..
# Running Main Agent 3: Assistant Agent finished using tool get_user_info with result: User Name: Amraha, Email: amraha@gmail.com

# Tool output: User Name: Amraha, Email: amraha@gmail.com
# Running Main Agent 4: Assistant Agent Finished with output: I know your name is Amraha, and your email is amraha@gmail.com. How can I assist you today?

# Message Output:
#  'I know your name is Amraha, and your email is amraha@gmail.com. How can I assist you today?'

# Final Result: I know your name is Amraha, and your email is amraha@gmail.com. How can I assist you today?
