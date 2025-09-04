from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    RunContextWrapper,
    OutputGuardrailTripwireTriggered,
    GuardrailFunctionOutput,
    output_guardrail,
    RunConfig
)
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import asyncio

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

class FinalResponse(BaseModel):
    response: str

class PoliticsRelated(BaseModel):
    is_politics : bool
    reasoning : str

guardrail_agent = Agent(
    name = "Guardrail Agent",
    instructions = "You are a output guardrail Agent. Make sure Agent's output should not contain politics related response.",
    output_type = PoliticsRelated
)

@output_guardrail
async def PoliticsGuardrail(ctx : RunContextWrapper, agent: Agent, output: FinalResponse)-> GuardrailFunctionOutput:
    result = await Runner.run(
        guardrail_agent,
        output.response,
        context = ctx.context,
        run_config = config
    )

    return GuardrailFunctionOutput(
        output_info = result.final_output,
        tripwire_triggered = result.final_output.is_politics
    )

agent = Agent(
    name= "Customer support Agent",
    instructions = "You are a customer support agent. You help customers with their questions.",
    output_guardrails = [PoliticsGuardrail],
    output_type =FinalResponse
)

async def main():
    try:
        result = await Runner.run(
            agent,
            "Name the biggest city of Pakistan",
            run_config = config
        )
        print("Output Guardrail's Tripwire didn't Triggered!")
        print(result.final_output)

    except OutputGuardrailTripwireTriggered:
        print("Politics Output Guardrail Tripped!")

    try:
        result = await Runner.run(
            agent,
            "What is going on in politics now adays",
            run_config = config
        )
        print("Output Guardrail's Tripwire didn't Triggered!")
        print(result.final_output)

    except OutputGuardrailTripwireTriggered:
        print("Politics Output Guardrail Tripped!")

asyncio.run(main())



# OUTPUT 👇🏻

# Output Guardrail's Tripwire didn't Triggered!
# response='Karachi


# Politics Output Guardrail Tripped!
