from agents import (
    Agent,
    output_guardrail,
    input_guardrail,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    TResponseInputItem,
    RunContextWrapper,
    Runner
)
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio

load_dotenv()

class ChemistryInputSchema(BaseModel):
    is_chemistry: bool
    reasoning: str

class ChemistryOutputSchema(BaseModel):
    is_chemistry: bool
    reasoning: str

class FinalResponse(BaseModel):
    response: str

chem_input_guardrail = Agent(
    name = "Input Guardrail",
    instructions =" Determine if the input is related to chemistry. If it is, set 'is_chemistry' to true"
     " If not, set 'is_chemistry' to false and provide reasoning.",
    model = 'gpt-4o-mini',
    output_type = ChemistryInputSchema,
)

chem_output_guardrail = Agent(
    name = "Output Guardrail",
    instructions = " Determine if the response is related to chemistry. If it is, set 'is_chemistry' to true"
     " If not, set 'is_chemistry' to false and provide reasoning.",
    model = 'gpt-4o-mini',
    output_type = ChemistryOutputSchema,    
)

@input_guardrail
async def input_chem_func(
        ctx: RunContextWrapper[None], 
        agent: Agent, 
        input: str | list[TResponseInputItem]
    ) -> GuardrailFunctionOutput:
        result = await Runner.run(
            chem_input_guardrail,
            input = input,
            context = ctx.context
    )
        return GuardrailFunctionOutput(
            output_info = result.final_output,
            tripwire_triggered = result.final_output.is_chemistry,
)

@output_guardrail
async def output_chem_func(
        ctx: RunContextWrapper, 
        agent: Agent, 
        output : FinalResponse
    ) -> GuardrailFunctionOutput:
        result = await Runner.run(
            chem_output_guardrail,
            output.response,
            context = ctx.context
    )
        return GuardrailFunctionOutput(
            output_info = result.final_output,
            tripwire_triggered = result.final_output.is_chemistry,
    )

main_agent = Agent(
    name = "Main Agent",
    instructions = "You are a helpful assistant. Answer the question to the best of your ability.",
    model = 'gpt-4o-mini',
    output_type = FinalResponse,
    input_guardrails = [input_chem_func],
    output_guardrails = [output_chem_func],
)

async def main():
    try:
        result = await Runner.run(
            main_agent,
            input = "Explain briefly the process of photosynthesis.",
        )
        print(f"Final Output:\n\t{result.final_output}\n")
    except InputGuardrailTripwireTriggered:
        print(f"\nInput should not related to chemistry :) \n")

    except OutputGuardrailTripwireTriggered:
        print(f"\nOops! Output is having Chemistry related content:( \n")

asyncio.run(main())


# OUTPUT 👇🏻:
# Input should not related to chemistry :) 