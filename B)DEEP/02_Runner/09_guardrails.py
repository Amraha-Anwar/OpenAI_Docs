from agents import (
    Agent,
    Runner,
    input_guardrail,
    output_guardrail,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    GuardrailFunctionOutput,
    TResponseInputItem,
    RunContextWrapper
)
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio

load_dotenv()

class FinalResponse(BaseModel):
    response: str

class PoliticsOutput(BaseModel):
    is_politics_output: bool
    reasoning: str

class PoliticsInput(BaseModel):
    is_politics_input: bool
    reasoning: str

politics_input_guardrail = Agent(
    name = "Politics Guardrail Agent",
    instructions = "You are a Politics Guardrail Agent"
    "Check User's Input text if it includes something politics related"
    "If it does, take it as a prohibited query and raise InputGuardrailTripwireTriggered exception."
    "Otherwise, Help user with their query.",
    output_type = PoliticsInput,
    model = 'gpt-4o-mini'
)

politics_output_guardrail = Agent(
    name= "Politics Output Guardrail Agent",
    instructions ="You are a Politics Guardrail Agent"
    "Verify that LLM's final response should not related to politics at all"
    "If llm's response have something politics related information mark it as a prohibited output and raise OutputGuardrailTripwireTriggered exception."
    "Otherwise, pass the response to the user as it is.",
    output_type = PoliticsOutput,
    model = 'gpt-4o-mini'
)

@input_guardrail
async def input_guardrail_func(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        politics_input_guardrail,
        input = input,
        context = ctx.context
    )
    return GuardrailFunctionOutput(
        output_info = result.final_output,
        tripwire_triggered = result.final_output.is_politics_input
    )

@output_guardrail
async def output_guardrail_func(
    ctx: RunContextWrapper[None],
    agent: Agent,
    output: FinalResponse
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        politics_output_guardrail,
        output.response,
        context = ctx.context
    )
    return GuardrailFunctionOutput(
        output_info = result.final_output,
        tripwire_triggered = result.final_output.is_politics_output
    )

Triage_agent = Agent(
    name = "Triage Agent",
    instructions = "You are a main User Helper Agent"
    "First of all check user's input text if it includes politics related question use input guardrail to block user's query"
    "If user's query is not related to politics process it further"
    "Then make sure llm's final response should not include politics related information, if so restrict the llm to pass the response to user."
    "Otherwise help user as much as you can to solve their problem.",
    input_guardrails = [input_guardrail_func],
    output_guardrails = [output_guardrail_func],
    model = 'gpt-4o-mini',
    output_type = FinalResponse
)

async def main():
    try:
        print("TEST QUERY 1: --- What is happening currently in India's political world? ---")
        output1 = await Runner.run(
            Triage_agent,
            "What is happening currently in India's political world?"
        )
        print(f"1st Query's Response:\n{output1.final_output}")

        print("TEST QUERY 2: ---What is the name of The largest mountain of the world?---")
        output2 = await Runner.run(
            Triage_agent,
            "What is the name of The largest mountain of the world?"
        )
        print(f"2nd Query's Response:\n{output2.final_output}")
    except InputGuardrailTripwireTriggered:
        print("---Input Guardrail Tripped...I can't help you with this query---")

    except OutputGuardrailTripwireTriggered:
        print("---Output Guardrail Tripped...My Response include something which is not allowed to deliver---")


asyncio.run(main())


# OUTPUT 👇🏻

# TEST QUERY 1: --- What is happening currently in India's political world? ---
# ---Input Guardrail Tripped...I can't help you with this query---

## NOTE 📌
# first query involves something that is prohibited according to input guardrail so it won't process further
# and will stop further processing

