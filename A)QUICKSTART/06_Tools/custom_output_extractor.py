from agents import Agent, Runner, RunResult
from dotenv import load_dotenv
import asyncio

load_dotenv()

turkish_agent = Agent(
    name="Turkish Speaker",
    instructions="You are turkish speaking Agent. Reply user in Turkish Language.",
    model='gpt-4o-mini',
)

async def my_output(result: RunResult) -> str:
    print(f"Result: {result}")
    return "Hello! How are you Amraha?"

triage_agent = Agent(
    name="Triage Agent",
    instructions="You are a helpful assistant. Help user with their query.",
    tools=[
        turkish_agent.as_tool(
            tool_name="translate_to_turkish",
            tool_description="Translate text into turkish.",
            custom_output_extractor=my_output
        )
    ],
    model='gpt-4o-mini',
    tool_use_behavior = 'stop_on_first_tool'
)

async def main():
    result = await Runner.run(
        starting_agent = triage_agent,
        input = "translate 'I am happy because I'm having a good day today' into turkish."
    )
    print(f"Final Response: {result.final_output}")
    
asyncio.run(main())


# OUTPUT 👇🏻
# Result: RunResult:
# - Last agent: Agent(name="Turkish Speaker", ...)
# - Final output (str):
#     Bunun için çok sevindim! Güzel bir gün geçirmen harika. Bugünün seni neşelendiren özel bir durumu var mı?
# - 1 new item(s)
# - 1 raw response(s)
# - 0 input guardrail result(s)
# - 0 output guardrail result(s)
# (See `RunResult` for more details)

# Final Response: The translation of "I am happy because I'm having a good day today" into Turkish is: "Bugün güzel bir gün geçiriyorum, bu yüzden mutluyum."


# OUTPUT by setting (tool_use_behavior = 'stop_on_first_tool') 👇🏻
# Result: RunResult:
# - Last agent: Agent(name="Turkish Speaker", ...)
# - Final output (str):
#     Bugün iyi bir gün geçirdiğin için mutlu olman harika! Umarım günün böyle devam eder. Başka bir konuda konuşmak ister misin?
# - 1 new item(s)
# - 1 raw response(s)
# - 0 input guardrail result(s)
# - 0 output guardrail result(s)
# (See `RunResult` for more details)

# Final Response: Hello! How are you Amraha?