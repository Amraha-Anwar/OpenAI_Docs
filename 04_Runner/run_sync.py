from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    RunConfig
)
from dotenv import load_dotenv
import os
import asyncio

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
    model="gemini-2.0-flash-exp",
    openai_client=client,
)

config = RunConfig(
    model= model,
    model_provider=client,
    tracing_disabled=True,
)

agent = Agent(
    name = "Gemini Agent",
    instructions = "You are a helpful assistant that can answer questions and help with tasks.",
    model = model,
)