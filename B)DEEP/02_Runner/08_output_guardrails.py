from agents import (
    Agent,
    Runner,
    output_guardrail,
    OutputGuardrailTripwireTriggered,
    GuardrailFunctionOutput,
    RunContextWrapper,

    function_tool
)
from typing import Union
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio

load_dotenv()

# structured data
class MedicinesPrescribed(BaseModel):
    medicine1: str
    medicine2: str
    medicine3: str

class PatientInfo(BaseModel):
    patient_name: str
    bed_no: int
    disease: str
    is_recovering: bool
    medicine_prescribed: MedicinesPrescribed

class FinalResponse(BaseModel):
    response: str

# Unified class for the agent's output
class AgentOutput(BaseModel):
    output: Union[PatientInfo, FinalResponse]


class SelfMedication(BaseModel):
    is_self_medication_related: bool
    reasoning: str


@function_tool
def get_patient_info(ctx: RunContextWrapper):
    """
    Use this tool to get the complete details of the patient stored in the context.
    Returns the patient's name, bed number, disease, recovery status, and prescribed medicines.
    """
    return ctx.context

selfMedication_guardrail_agent = Agent(
    name="Self-Medication Guardrail",
    instructions="You are a medical safety checker. "
                 "Analyze the provided **AI response**. "
                 "If the response contains a list of medicines, a prescription, or suggests any medical treatment, classify it as self-medication."
                 "Otherwise, mark it as safe.",
    model='gpt-4o-mini',
    output_type=SelfMedication
)

@output_guardrail
async def output_guardrail_function(
    ctx: RunContextWrapper[None],
    agent: Agent,
    output: AgentOutput 
) -> GuardrailFunctionOutput:
    if isinstance(output.output, FinalResponse):
        result = await Runner.run(
            selfMedication_guardrail_agent,
            output.output.response,
        )
        return GuardrailFunctionOutput(
            output_info=result.final_output,
            tripwire_triggered=result.final_output.is_self_medication_related
        )
    
    return GuardrailFunctionOutput(
        output_info=None,
        tripwire_triggered=False
    )

async def main():
    try:
        agent = Agent(
            name="Assistant Agent",
            instructions=(
                "You are a hospital assistant AI. "
                "If the user asks for patient details, use the **PatientInfo** structure from the context. "
                "For any other query, use the **FinalResponse** structure to provide a safe, non-prescriptive answer. "
                "You are not allowed to recommend or invent new medicines."
            ),
            model="gpt-4o-mini",
            output_type=AgentOutput, 
            output_guardrails=[output_guardrail_function],
            tools=[get_patient_info]
        )
        
        patient_information = PatientInfo(
            patient_name="William",
            bed_no=324,
            disease="Heart Attack",
            is_recovering=True,
            medicine_prescribed=MedicinesPrescribed(
                medicine1="med123", medicine2="med456", medicine3="med789"
            )
        )
        
        # Test 1: Query for patient details. This should use the tool and return a PatientInfo object.
        print("--- Query: Give me the complete detail of the patient ---")
        result_patient_info = await Runner.run(
            agent,
            "Give me the complete details of the patient",
            context=patient_information
        )
        print(result_patient_info.final_output)

        print("\n--- Query: Can you suggest me 3 medicines for heart disease? ---")
        # Test 2: Query for medical advice. This should trigger the guardrail.
        result_medication_advice = await Runner.run(
            agent,
            "Can you suggest me 3 medicines for heart disease?",
            context=patient_information
        )
        print(result_medication_advice.final_output)

    except OutputGuardrailTripwireTriggered:
        print("⚠️ Sorry, I cannot provide self-medication advice. Please consult a qualified doctor.")

asyncio.run(main())


# OUTPUT 👇🏻

# --- Query: Give me the complete detail of the patient ---
# output=PatientInfo(patient_name='William', bed_no=324, disease='Heart Attack', is_recovering=True, medicine_prescribed=MedicinesPrescribed(medicine1='med123', medicine2='med456', medicine3='med789'))

# --- Query: Can you suggest me 3 medicines for heart disease? ---
# output=FinalResponse(response="I'm unable to recommend specific medicines for heart disease. It's important to consult with a healthcare professional for appropriate diagnosis and treatment options.")