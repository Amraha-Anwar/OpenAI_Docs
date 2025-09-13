from agents import (
    Agent,
    Runner,
    input_guardrail,
    InputGuardrailTripwireTriggered,
    TResponseInputItem,
    GuardrailFunctionOutput,
    RunContextWrapper,
    AgentOutputSchema,
    function_tool
)
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio

load_dotenv()

# for structured output
class MedicinesPrescribed(BaseModel):
    medicine1 : str
    medicine2: str
    medicine3: str

# for structured output
class PatientInfo(BaseModel):
    patient_name: str
    bed_no : int
    disease: str
    is_recovering: bool
    medicine_prescribed : MedicinesPrescribed


class SelfMedication(BaseModel):
    is_self_medication_related : bool
    reasoning: str


@function_tool
def get_patient_info(ctx: RunContextWrapper):
    """
    Use this tool to get the complete details of the patient stored in the context.
    Returns the patient's name, bed number, disease, recovery status, and prescribed medicines.
    """
    return ctx.context

selfMedication_guardrail_agent = Agent(
    name = "Self-Medication Guardrail",
    instructions = " You are a medical safety checker." 
    "If the user is asking for medicines or prescriptions without mentioning a doctor's consultation or medical professional, classify it as self-medication."
    "Otherwise, mark it as safe.",
    model = 'gpt-4o-mini',
    output_type = SelfMedication
)

@input_guardrail
async def input_guardrail_function(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input : str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        selfMedication_guardrail_agent,
        input = input
    )
    return GuardrailFunctionOutput(
        output_info = result.final_output,
        tripwire_triggered = result.final_output.is_self_medication_related
    )


patient_information = PatientInfo(patient_name="William", bed_no=324, disease="Heart Attack", is_recovering=True, medicine_prescribed=MedicinesPrescribed(medicine1="med123", medicine2="med456", medicine3="med789"))

async def main():
    try:
        agent = Agent(
            name = "Assistant Agent",
            instructions ="You are a hospital assistant AI." 
                "You can only work with already provided **patient records** (like patient name, bed number, disease, stage, or prescribed medicines)."
                "You are not allowed to recommend or invent new medicines on your own." 
                "If asked about medical treatment, you must strictly rely on the structured PatientInfo data that is already given."
                "If a user requests medicines without doctor consultation, pass the query through the input guardrail."
                "- Provide general health, recovery, or lifestyle advice that is safe and non-prescriptive.",
            model = "gpt-4o-mini",
            output_type = AgentOutputSchema(PatientInfo, strict_json_schema=True),
            input_guardrails = [input_guardrail_function],
            tools=[get_patient_info]
            )
        result = await Runner.run(
            agent,
            "Can you suggest me 3 medicines for heart disease?",
            # "Give me the complete details of the patient",
            # context = patient_information
            context = patient_information

        )
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("⚠️ Sorry, I cannot provide self-medication advice. Please consult a qualified doctor.")


asyncio.run(main())


# OUTPUT 👇🏻

# patient_name='William' bed_no=324 disease='Heart Attack' is_recovering=True medicine_prescribed=MedicinesPrescribed(medicine1='med123', medicine2='med456', medicine3='med789')



# OUTPUT when asked for the medication suggestion 👇🏻
# ⚠️ Sorry, I cannot provide self-medication advice. Please consult a qualified doctor.