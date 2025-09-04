from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled ,Runner, function_tool
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
    model = 'gemini-2.0-flash',
    openai_client = external_client,
)

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is hot."

agent = Agent(
    name = "Assistant Agent",
    instructions = "Always respond in Haiku form.",
    model = model,
    tools = [get_weather]
)

async def main():
    result = await Runner.run(
        agent,
        "What is the current weather of Karachi?"
    )

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())


# OUTPUT 👇🏻
# Karachi is hot
# The weather is not so nice
# Stay cool, drink water