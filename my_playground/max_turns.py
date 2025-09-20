from dis import Instruction
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
import asyncio

load_dotenv()

@function_tool
def doubler(num: int) -> str:
    """takes argument from user's text and double it.
    
    Args:
        num: number which will be doubled
    """
    return f"The double of {num} is '{num*2}'"


italian_agent = Agent(
    name = "Italian Speaker",
    instructions = "You are an Italian Agent. You always reply in Italian Language.",
    model = 'gpt-4o-mini'
)

agent = Agent(
    name = "Problem Solver",
    instructions="You are a problem solver agent. Solve user's query"
    "If user ask to double any number you must have to use tool [doubler]. Don't answer by yourself."
    "If user want you to reply in Italian, handoff to [italian_agent]. Don't answer by yourself.",
    model = "gpt-4o-mini",
    tools = [doubler],
    handoffs = [italian_agent],
    # tool_use_behavior = "stop_on_first_tool"
)

async def main():
    response = await Runner.run(
        agent,
        "What is the double of 355? Also write a greeting message for my friend in Italian.",
        # max_turns = 1 
    )

    print(response.final_output)
    print(response.last_agent.name)

asyncio.run(main())


# OUTPUT 👇🏻

# ll doppio di 355 è 710. 

# Ecco un messaggio di saluto per il tuo amico in italiano:

# "Ciao! Spero che tu stia bene e che la tua giornata sia fantastica! A presto!"
# Italian Speaker


# 📌 We can run an agent with a tool in 1 turn by setting tool_use_behavior = "stop_on_first_tool".
# but with the sub-agent  (handoff concept), we can pass the sub-agents as tools then set the tool_use_behavior to 'stop_on_first_tool'.