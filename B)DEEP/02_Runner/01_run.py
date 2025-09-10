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
enable_verbose_stdout_logging()

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
    result = await Runner.run(
        starting_agent = main_agent,
        input = "What do you know about me?",
        max_turns = 5,
        hooks = CustomRunHook("Running Main Agent"),
        context = UserInfo(name= "Amraha", email = "amraha@gmail.com")
        )
    
    print("\nFinal Result:", result.final_output)

asyncio.run(main())

# OUTPUT 👇🏻

# Running Main Agent 1: Assistant Agent Started..
# Running Main Agent 2: Assistant Agent using tool get_user_info..
# Running Main Agent 3: Assistant Agent finished using tool get_user_info with result: User Name: Amraha, Email: amraha@gmail.com
# Running Main Agent 4: Assistant Agent Finished with output: I know that your name is Amraha and your email is amraha@gmail.com. How can I assist you today?

# Final Result: I know that your name is Amraha and your email is amraha@gmail.com. How can I assist you today?