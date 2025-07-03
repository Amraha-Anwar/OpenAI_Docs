from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, set_tracing_disabled, RunContextWrapper
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
set_tracing_disabled(disabled = True)

gemini_key = os.getenv("GEMINI_API_KEY")
url = os.getenv("BASE_URL")

client = AsyncOpenAI(
    api_key = gemini_key,
    base_url = url
)

model = OpenAIChatCompletionsModel(
    model = 'gemini-2.5-flash',
    openai_client = client
)

class userContext(BaseModel):
    name: str
    hobbies: list[str]

def dynamic_instructions(wrapper: RunContextWrapper[userContext], agent: Agent[userContext]) -> str:
    return f"The user's name is {wrapper.context.name}, say 'hello' by mentioning their name then help them with their query in a polite manner."

user_context = userContext(name = "Amraha", hobbies = ["Reading", "Coding"])


agent = Agent[userContext](
    name = "Helper Agent",
    instructions = dynamic_instructions,
    model = model
)

async def main():
    result = await Runner.run(
        agent,
        "How to pitch clients on LinkedIn? specilly for Web Development services.",
        context = user_context
    )

    print(result.final_output)

asyncio.run(main())