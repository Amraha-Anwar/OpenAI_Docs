from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, RunContextWrapper, AgentHooks, set_tracing_disabled
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
set_tracing_disabled(True)
gemini_api_key = os.getenv("GEMINI_API_KEY")
url = os.getenv("BASE_URL")
MODEL = 'gemini-2.5-flash'

client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url = url
)

model = OpenAIChatCompletionsModel(
    model = MODEL,
    openai_client = client
)

class CustomAgentHooks(AgentHooks):
    def __init__(self, agent_name: str):
        self.event_counter = 0
        self.agent_name = agent_name

    async def on_start(self, ctx:RunContextWrapper, agent:Agent) -> None:
        self.event_counter += 1
        print(f"{self.agent_name} {self.event_counter}:\n{agent.name} Started!")

    async def on_end(self, ctx:RunContextWrapper, agent: Agent, output: any) -> None:
        self.event_counter += 1
        print(f"{self.agent_name} {self.event_counter}:\n{agent.name} Ended with output:\n{output}")

    async def on_handoff(self, ctx:RunContextWrapper, agent:Agent, source: Agent)-> None:
        self.event_counter += 1
        print(f"{self.agent_name} {self.event_counter}:\n{source.name} handed off to {agent.name}")


multiplier_agent = Agent(
    name = "Multiplier Agent",
    instructions = "You are a Multiplier Agent. Take Number from user's input and multiply the Number by 2 then return the final result.",
    hooks = CustomAgentHooks(agent_name="Multiplier Agent"),
    model = model
)

start_agent = Agent(
    name="Main Agent",
    instructions="You are a helper Agent. Help user with their query. If user ask to double any number, handoff to the [multiplier agent] and show the final result.",
    handoffs=[multiplier_agent],
    hooks=CustomAgentHooks(agent_name="Main Agent"),
    model=model

)


async def main():
    await Runner.run(
        start_agent,
        input=f"What is the double of 4?",
    )

    print("Done!")


asyncio.run(main())
     

# OUTPUT 👇🏻

# Main Agent 1:
# Main Agent Started!
# Main Agent 2:
# Main Agent handed off to Multiplier Agent
# Multiplier Agent 1:
# Multiplier Agent Started!
# Multiplier Agent 2:
# Multiplier Agent Ended with output:
# I am a Multiplier Agent. The double of 4 is 8.
# Done!