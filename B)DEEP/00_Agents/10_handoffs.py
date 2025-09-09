from agents  import (
    Agent, 
    Runner,
    enable_verbose_stdout_logging,
)
from dotenv import load_dotenv
from rich import print
import asyncio

load_dotenv()
# enable_verbose_stdout_logging()

tutor_agent = Agent(
    name="Tutor",
    instructions="You are a helpful tutor who assists students with their questions related to their studies.",
    model='gpt-4o-mini',
)

email_agent = Agent(
    name="Email",
    instructions="You are an email assistant. You help users manage their emails, including composing, replying, and organizing messages.",
    model='gpt-4o-mini',
)

triage_agent = Agent(
    name="Triage",
    instructions="You are a triage assistant. You help route user queries to the appropriate agent based on the content of the query.",
    model='gpt-4o-mini',
    handoffs = [tutor_agent, email_agent]
)

user_queries = "I need to reply to an email from my professor about the assignment."
               # "Can you help me understand the Pythagorean theorem?"
async def main():
    result = await Runner.run(triage_agent, user_queries)
    print(result.final_output)

asyncio.run(main())  
