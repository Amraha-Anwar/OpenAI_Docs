from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunContextWrapper, RunHooks, set_tracing_disabled
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

class TestRunHook(RunHooks):
    def __init__(self):
        self.event_counter = 0
        self.name = "Test Hook"

    async def on_agent_start(self, context:RunContextWrapper, agent:Agent )->None:
        self.event_counter += 1
        print(f"{self.name} {self.event_counter}:\n{agent.name} Started!\nUsage:{context.usage}\n")

    async def on_agent_end(self, context:RunContextWrapper, agent:Agent, output:any)-> None:
        self.event_counter += 1
        print(f"{self.name} {self.event_counter}:\n{agent.name} Ended!\nUsage:{context.usage}\nOUTPUT:\n\n{output}\n")

    async def on_handoff(self, context:RunContextWrapper, from_agent: Agent, to_agent: Agent)->None:
        self.event_counter += 1
        print(f"{self.name} {self.event_counter}:\n{from_agent.name} handed off to {to_agent.name}\nUsage: {context.usage} \n")
    

hook = TestRunHook()

spanish_agent = Agent(
    name = "Spanish Agent",
    instructions = "You are a spanish Agent. Convert user's input text into Spanish.",
    model = model
)

main_agent = Agent(
    name = "Query Solver Agent",
    instructions = "You are an agent who solves user's queries. If user ask to translate something in Spanish, handoff to the [spanish_agent]. If user ask about anything else YOU have to answer that.",
    model = model,
    handoffs = [spanish_agent]
)

async def main():
    await Runner.run(
        main_agent,
        "convert 'hello I am Amraha, an Agentic AI Developer' into spanish.",
        hooks = hook
    )


asyncio.run(main())


# OUTPUT 👇🏻

# Test Hook 1:
# Query Solver Agent Started!
# Usage:Usage(requests=0, input_tokens=0, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=0, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=0)

# Test Hook 2:
# Query Solver Agent handed off to Spanish Agent
# Usage: Usage(requests=1, input_tokens=100, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=14, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=162)

# Test Hook 3:
# Spanish Agent Started!
# Usage:Usage(requests=1, input_tokens=100, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=14, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=162)

# Test Hook 4:
# Spanish Agent Ended!
# Usage:Usage(requests=2, input_tokens=175, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=32, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=389)
# OUTPUT:

# ¡Hola! Soy Amraha, una Desarrolladora de IA Agéntica.