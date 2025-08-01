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

result = Runner.run_sync(agent, "what is meant by the term 'AI'? Brief description in Roman Urdu", run_config=config)
print(result.final_output)

# OUTPUT 👇🏻

# AI se muraad hai "Artificial Intelligence." Yeh ek technology hai jis mein computers aur machines ko insani dimagh ki tarah kaam karne ke liye banaya jata hai, jaise ke seekhna, faislay karna, aur masail hal karna.
