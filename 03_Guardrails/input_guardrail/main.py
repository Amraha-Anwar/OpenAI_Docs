from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    RunContextWrapper,
    InputGuardrailTripwireTriggered,
    GuardrailFunctionOutput,
    TResponseInputItem,
    input_guardrail,
    RunConfig
)
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
url = os.getenv("Base_URL")


if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")
     

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=url,
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

class PoliticsOutput(BaseModel):
    is_politics : bool
    reasoning: str

guardrail_agent = Agent(
    name = "Guardrail Agent",
    instructions = "Check if the user is asking about politics.",
    output_type = PoliticsOutput
)

@input_guardrail
async def politics_guardrail(
    ctx: RunContextWrapper[None], agent:Agent, input: str |list[TResponseInputItem]
    )-> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context= ctx.context, run_config = config)

    return GuardrailFunctionOutput(
        output_info = result.final_output,
        tripwire_triggered = result.final_output.is_politics
    )

agent = Agent(
    name = "Helpful Assistant",
    instructions = "You are a helpful Assistant. Solve user's query",
    input_guardrails = [politics_guardrail]
)

async def main():
    try:
        result = await Runner.run(agent, "Hello, what is happening in politic world now a days?", run_config = config)
        print("Guardrail didn't trip - this is unexpected")
        print(result.final_output)

    except InputGuardrailTripwireTriggered:
        print("Politics guardrail tripped")

asyncio.run(main())


# OUTPUT When I asked about politics 👇🏻
# Politics guardrail tripped


# OUTPUT When I said 'Hello' 👇🏻
# Guardrail didn't trip - this is unexpected
# Hello! How can I help you today?