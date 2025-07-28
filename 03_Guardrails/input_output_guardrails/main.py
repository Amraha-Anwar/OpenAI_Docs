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
import os


# configurations
load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')
url = os.getenv("BASE_URL")
MODEL = 'gemini-2.5-flash'

client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url = url
)

model = OpenAIChatCompletionsModel(
    model = MODEL,
    openai_client = client
)

config = RunConfig(
    model_provider = model,
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
    "You are a input Guardrail Agent. Check User's input if it is cooking related or not"
    "if user's input is related to cooking or baking return an structured output with 'CookingRelatedOutput' as boolean and your final result as reasoning.",
    output_type = CookingRelatedOutput
)

# output guardrail agent
outputGuardrail_agent = Agent(
    name = "Output Guardrail Agent"
)

@input_guardrail
async def cooking_related_guardrail(
    ctx: RunContextWrapper[None],
    agent : Agent,
    input : str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        inputGuardrail_agent, input, context = ctx.context, run_config = config)
    final_output = result.final_output_as(CookingRelatedOutput)
    output_info= final_output
    tripwire_triggered = not final_output.is_cooking_input  #agr user ka input cooking related nhi hua to ye trigger hoga

cook_agent = Agent(
    name = "Cook Agent",
    instructions = "You are a Cook Agent. Help User if they ask anything cooking related"
    "Answer accuratley and consicely",
    model = model,
    input_guardrails =cooking_related_guardrail
)