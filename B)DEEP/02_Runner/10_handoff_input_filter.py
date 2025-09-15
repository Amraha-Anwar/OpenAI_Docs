from agents import Agent, Runner, function_tool, handoff, HandoffInputData
from dotenv import load_dotenv

load_dotenv()

def summarized_user_input(data: HandoffInputData) -> HandoffInputData:
    print("\n---Handing off to Spanish Agent---\n")
    summarize_input = "User wants the text to be tranlated into Spanish."

    print(f"\n[ITEM 1]: {data.input_history}")
    print(f"\n[ITEM 2]: {data.pre_handoff_items}")
    print(f"\n[ITEM 3]: {data.new_items}")

    return HandoffInputData(
        input_history=summarize_input,
        pre_handoff_items=(),
        new_items=(),
    )


@function_tool
def add(a:int, b:int)-> str:
    "Returns the sum of 2 numbers"
    return f"The sum of {a} and {b} is = {a + b}."


spanish_agent = Agent(
    name = "Spanish Speaking Agent",
    instructions = "You are a Spanish Agent. You translate user's given text into spanish",
    model = 'gpt-4o-mini'
)

math_agent = Agent(
    name = "Math Expert",
    instructions= "You are the expert of maths. Solve user's math related query by must using the tool [add] if needed."
    "For Spanish related queries let spanish agent handle the task",
    model = 'gpt-4o-mini',
    tools = [add],
    handoffs = [handoff(agent=spanish_agent, input_filter=summarized_user_input)]
)

result = Runner.run_sync(
    math_agent,
    "translate 'have a nice day' into spanish."
)

print(f"Last Agent: '{result.last_agent.name}'\n")
print(f"Final Output: '{result.final_output}'\n")


# OUTPUT 👇🏻


# ---Handing off to Spanish Agent---

# [ITEM 1]: translate 'have a nice day' into spanish.

# [ITEM 2]: ()

# [ITEM 3]: (HandoffCallItem(agent=Agent(...........)

# Last Agent: 'Spanish Speaking Agent'

# Final Output: 'Por supuesto, proporciona el texto que deseas traducir al español.'