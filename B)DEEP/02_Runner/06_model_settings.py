from agents import Agent, Runner, ModelSettings, function_tool, RunConfig
from dotenv import load_dotenv
from rich import print
import asyncio

load_dotenv()


Model_Settings = ModelSettings(
        temperature = 0.75,
        top_p = 0.1,
        presence_penalty = 0.8,
        frequency_penalty = 0.75,
        tool_choice = "none",
        parallel_tool_calls = False,
        truncation = "auto",
        max_tokens = 250,
        verbosity = 'medium',
    )

config = RunConfig(
    model = 'gpt-4o-mini',
    # model_provider  {defaults to OpenAI}
    model_settings = Model_Settings,
)

agent = Agent(
    name = "Story Writer",
    instructions = "You are an expert story writer. Write short, interesting and engaging stories for kids on the given topic.",
    model = 'gpt-4o-mini'
)

async def main():
    result = await Runner.run(
        agent,
        "Write a short story on 'a flying mat'.",
        run_config = config
    )

    print(result.final_output)

asyncio.run(main())