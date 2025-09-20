from agents import Agent, Runner, function_tool, ModelSettings, RunConfig
from dotenv import load_dotenv
import asyncio

load_dotenv()

config = RunConfig(
    model_settings = ModelSettings(
        parallel_tool_calls = False
    )
)

@function_tool
def doubler(num: int) -> str:
    """takes argument from user's text and double it.
    
    Args:
        num: number which will be doubled
    """
    return f"The double of {num} is '{num*2}'"

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You translate the user's message to Spanish",
    model = 'gpt-4o-mini'
)

french_agent = Agent(
    name="French agent",
    instructions="You translate the user's message to French",
    model = 'gpt-4o-mini'

)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools."
    ),
    tools = [
        spanish_agent.as_tool(
            tool_name = "translate_to_spanish",
            tool_description = "Translate user's text to Spanish."
        ),
        french_agent.as_tool(
            tool_name = "translate_to_french",
            tool_description = "Translate user's text to french."
        ),
        doubler
    ],
    model = 'gpt-4o-mini',
    # tool_use_behavior = 'stop_on_first_tool'
)

async def main():
    result = await Runner.run(
        orchestrator_agent,
        "what is the double of 5? and also Say 'Hello, how are you?' in Spanish.",
        # max_turns = 1,
        run_config = config
)
    print(result.final_output)


asyncio.run(main())