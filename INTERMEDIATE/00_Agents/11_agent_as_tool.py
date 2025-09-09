from agents import Agent, Runner, RunResult
from dotenv import load_dotenv
from rich import print
import asyncio

load_dotenv()

turkish_agent = Agent(
    name="Turkish Language Agent",
    instructions="An agent that translates English text to Turkish.",
    model = "gpt-4o-mini",
)

italian_agent = Agent(
    name="Italian Language Agent",
    instructions="An agent that translates English text to Italian.",
    model = "gpt-4o-mini",
)


async def turkish_final_answer(result: RunResult) -> str:
      return "This is custom_output_extractor function for Turkish Agent."

orchestrator_agent = Agent(
    name="Orchestrator Agent",
    instructions="You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools",
    model = "gpt-4o-mini",
    tool_use_behavior="stop_on_first_tool",
    tools = [
        turkish_agent.as_tool(
            tool_name="translate_to_turkish",
            tool_description="Translate the user's text to Turkish.",
            custom_output_extractor=turkish_final_answer
        ),
        italian_agent.as_tool(
            tool_name="translate_to_italian",
            tool_description="Translate the user's text to Italian."
        )
    ],
)


result = Runner.run_sync(
        orchestrator_agent,
        "'Hello, how are you?', translate it into Turkish.",
    )
print(result.final_output)




# OUTPUT 👇🏻
# The translation of "Hello, how are you?" to Turkish is: **Merhaba, nasılsın?**