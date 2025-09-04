from agents import Agent, ModelSettings
from agents.run import Runner
from dotenv import load_dotenv
import asyncio

load_dotenv()

agent = Agent(
    name = "Assistant",
    instructions = "You are a user's personal Assistant. Help him/her with their query.",
    model = 'gpt-4o-mini',
    model_settings = ModelSettings(
        temperature = 1.0,
        top_p = 0.9,
        frequency_penalty = 0.7,
        presence_penalty = 0.7,
        max_tokens = 100,
        
    )
)

async def main():
    result = await Runner.run(
        agent,
        "Write a paragraph on 'A wise King'."
    )
    print(result.final_output)

asyncio.run(main())