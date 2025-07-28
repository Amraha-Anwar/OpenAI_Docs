from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    RunContextWrapper,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    input_guardrail,
    output_guardrail,
    TResponseInputItem,
    GuardrailFunctionOutput,
    RunConfig
)
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio
import os


# configurations
load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')
url = os.getenv("BASE_URL")
MODEL = 'gemini-2.0-flash'

client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url = url
)

model = OpenAIChatCompletionsModel(
    model = MODEL,
    openai_client = client
)

config = RunConfig(
    model = model,
    model_provider = client,
    tracing_disabled = True
)

# pydantic class for the final structured output
class FinalResponse(BaseModel):
    response : str

# pydantic class for user's input analysis and structured output
class CookingRelatedOutput(BaseModel):
    is_cooking_input : bool
    reasoning : str

# pydantic class for agent's output analysis and structured output
class CookingRelatedOutput2(BaseModel):
    is_cooking_output : bool
    reasoning : str

# input guardrail agent
inputGuardrail_agent = Agent(
    name = "Input Guardrail Agent",
    instructions = 
    "You are a input Guardrail Agent. Check User's input if it is cooking related or not."
    "if user's input is related to cooking return a structured output with 'CookingRelatedOutput' as boolean and your final result as reasoning.",
    output_type = CookingRelatedOutput
)

# output guardrail agent
outputGuardrail_agent = Agent(
    name = "Output Guardrail Agent",
    instructions = 
    "You are a output Guardrail Agent. Check if Agent's output is related to cooking or not."
    "if Agent's ouptut is related to cooking return a structured output with 'CookingRelatedOutput2' as boolean and your final result as reasoning.",
    output_type = CookingRelatedOutput2
)

# input guardrail function which will use input guardrail agent and handle output
@input_guardrail
async def cooking_input_guardrail(
    ctx: RunContextWrapper[None],
    agent : Agent,
    input : str | list
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        inputGuardrail_agent, input, context = ctx.context, run_config = config)
    final_output = result.final_output_as(CookingRelatedOutput)
    return GuardrailFunctionOutput(
        output_info= final_output,
        tripwire_triggered = not final_output.is_cooking_input  #agr user ka input cooking related nhi hua to ye trigger hoga
    )

# output guardrail function which will use output guardrail agent and handle output
@output_guardrail
async def cooking_output_guardrail(
    ctx: RunContextWrapper,
    agent : Agent,
    output : FinalResponse
) -> GuardrailFunctionOutput:
    result = await Runner.run(outputGuardrail_agent, output.response , context = ctx.context, run_config = config)
    final_output = result.final_output_as(CookingRelatedOutput2)
    return GuardrailFunctionOutput(
        output_info = final_output,
        tripwire_triggered = not final_output.is_cooking_output  #agr agent ka output cooking rlated nhi hua tb ye trigger hoga
    )

cook_agent = Agent(
    name = "Cook Agent",
    instructions = "You are a Cook Agent. Help User if they ask anything cooking related"
    "Answer accuratley and consicely",
    model = model,
    input_guardrails = [cooking_input_guardrail],
    output_guardrails = [cooking_output_guardrail],
    output_type = FinalResponse
)

async def main():
    try:
        result = await Runner.run(cook_agent, "generate a short story on 'an ambitious girl'.", run_config = config)
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("Input Guardrail Tripped:\n\tI am a cook Agent and unfortunately your input is not Cooking related :( ")
    except OutputGuardrailTripwireTriggered:
        print("Output Guardrail Tripped:\n\tOops! Agent's response is not cooking related :( ")

    try:
        result = await Runner.run(cook_agent, "Can you tell me the recipe of Biryani?", run_config = config)
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("Input Guardrail Tripped:\n\tI am a cook Agent and unfortunately your input is not Cooking related :( ")
    except OutputGuardrailTripwireTriggered:
        print("Output Guardrail Tripped:\n\tOops! Agent's response is not cooking related :( ")

asyncio.run(main())


# OUTPUT 👇🏻

# Input Guardrail Tripped:
#         I am a cook Agent and unfortunately your input is not Cooking related :( 

# response="I can help you with that. There are many regional variations of Biryani. To give you the best recipe, could you please specify which style you'd like? (e.g., Hyderabadi, Lucknowi, Sindhi, Kolkata, etc.) Or, would you prefer a simple, basic Biryani recipe?"


