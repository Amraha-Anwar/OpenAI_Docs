from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, Runner, AgentOutputSchema
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio
import os

load_dotenv()
set_tracing_disabled(disabled = True)

gemini = os.getenv("GEMINI_API_KEY")
url = os.getenv("BASE_URL")

client = AsyncOpenAI(
    api_key= gemini,
    base_url= url
)

model = OpenAIChatCompletionsModel(
    model = 'gemini-2.5-flash',
    openai_client = client
)

class CalenderEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

agent = Agent(
    name = "Reminder Agent",
    instructions = "Pull out events from input",
    model = model,
    output_type = AgentOutputSchema(output_type = CalenderEvent)
)

async def main():
    result = await Runner.run(
        agent, 
        "Monsoon is going to start on July 8, 2025"
    )
    print(result.final_output)

asyncio.run(main())