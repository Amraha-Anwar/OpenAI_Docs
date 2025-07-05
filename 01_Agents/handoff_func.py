from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled ,Runner, handoff, RunContextWrapper
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
set_tracing_disabled(disabled = True)

gemini_api_key = os.getenv("GEMINI_API_KEY")
url = os.getenv("BASE_URl")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=url,
)

model = OpenAIChatCompletionsModel(
    model = 'gemini-2.5-flash',
    openai_client = external_client,
)

library_agent = Agent(
    name = "Library Assistant Agent",
    instructions = """You are a Librarian, suggest some great Urdu and English Novel Names to user and also tell the user a short description of each Novel.""",
    handoff_description = "Suggest some great novels/books.",
    model = model,
)

advisor_agent = Agent(
    name = "Advisor Agent",
    instructions = """You are a great advisor, give some top freelancing Advises to User.""",
    handoff_description = "Give as best freelancing advises as you can.",
    model = model
)

def on_handoff(agent: Agent, ctx: RunContextWrapper[None]):
    agent_name = agent.name
    print (f"\n\t\tHANDING OFF TO {agent_name}\n")

orchestrator_agent = Agent(
    name = "Orchestrator Agent",
    instructions = 
    """give proper reply to the user."""
    """handoff to Library Agent if user is asking for any good book."""
    """handoff to Advisor Agent if user is asking for any freelancing tip."""
    """do apology on any other question.""",
    model = model,
    handoffs = [
        handoff(library_agent, on_handoff = lambda ctx:on_handoff(library_agent, ctx)),
        handoff(advisor_agent, on_handoff = lambda ctx:on_handoff(library_agent, ctx))
    ]
)

user_input = input("Ask me Anything: ")
async def main():
    result = await Runner.run(
        orchestrator_agent,
        input = user_input
    )

    print(result.final_output)

asyncio.run(main())