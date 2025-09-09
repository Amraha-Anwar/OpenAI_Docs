from agents import Agent, Runner, AsyncOpenAI, set_default_openai_key, set_default_openai_client
from dotenv import load_dotenv
import asyncio
import os


load_dotenv()

BASE_URL = 'https://api.openai.com/v1/openai'
API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    raise KeyError("OPENAI_API_KEY environment variable not set.")

Client = AsyncOpenAI(
    api_key = API_KEY,
    base_url = BASE_URL
)

set_default_openai_client(client = Client, use_for_tracing = False)

agent = Agent(
    name = "Assistant",
    instructions = "You are a helpful assistant.",
    model = "gpt-4o-mini"
)

async def main():
    result = await Runner.run(
        agent,
        "Hello!"
    )
    print(result.final_output)

asyncio.run(main())