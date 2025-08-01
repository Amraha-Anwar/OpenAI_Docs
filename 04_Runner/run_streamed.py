from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    RunConfig,
    enable_verbose_stdout_logging
)
from dotenv import load_dotenv
import os
import asyncio

# enable_verbose_stdout_logging()
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
url = os.getenv("BASE_URL")

if not gemini_api_key or not url:
    raise ValueError("GEMINI_API_KEY and BASE_URL must be set")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=url,
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client,
)

config = RunConfig(
    model= model,
    model_provider=client,
    tracing_disabled=True,
)

urdu_agent = Agent(
    name = "Urdu Agent",
    instructions = "You are a helpful assistant that can answer questions and help with tasks but in Roman Urdu.",
    handoff_description = "You are a helpful assistant that can answer questions in Roman Urdu.",
    model= model,
)

agent = Agent(
    name = "Gemini Agent",
    instructions = "You are a helpful assistant that can answer questions and help with tasks. Handoff to another agent if needed.",
    model = model,
    handoffs = [urdu_agent],
)

async def main():
    result = await Runner.run(agent, "what is meant by the term 'AI'?", run_config=config)

    async for event in result.stream_events():
        print(event)

asyncio.run(main())