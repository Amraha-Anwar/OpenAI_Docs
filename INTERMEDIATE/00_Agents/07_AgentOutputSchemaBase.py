from agents import (
    Agent,
    Runner,
    AgentOutputSchemaBase,
)
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio

load_dotenv()

class CustomOutputSchema(BaseModel):
    profession: str
    is_employed: bool
    years_of_experience: int

class CustomAgentOutputSchema(AgentOutputSchemaBase):
    def is_plain_text(self) -> bool:
        return False
    
    def name(self) -> str:
        return "CustomOutputSchema"
    
    def is_strict_json_schema(self) -> bool:
        return True
    
    def json_schema(self) -> dict:
        schema = CustomOutputSchema.model_json_schema()
        schema["additionalProperties"] = False 
        return schema
        
    def validate_json(self, json_obj:dict) -> any:
        return json_obj
    
agent = Agent(
    name="CustomOutputAgent",
    instructions="An agent that uses a custom output schema.",
    model="gpt-4o-mini",
    output_type=CustomAgentOutputSchema(),
)

async def main():
    result = await Runner.run(
        agent,
        input="Provide details about a software engineer whose is currently unemployed but has 5 years of experience.",
    )

    # print(result.final_output)
    print(f"\nOutput schema name: {CustomAgentOutputSchema().name()}\n")
    print(f"Is plain text: {CustomAgentOutputSchema().is_plain_text()}\n")
    print(f"Is strict JSON schema: {CustomAgentOutputSchema().is_strict_json_schema()}\n")
    print(f"JSON Schema: {CustomAgentOutputSchema().json_schema()}\n")
    print(f"Validated JSON: {CustomAgentOutputSchema().validate_json(result.final_output)}\n")

asyncio.run(main())

# OUTPUT👇🏻

# Output schema name: CustomOutputSchema

# Is plain text: False

# Is strict JSON schema: True

# JSON Schema: {'properties': {'profession': {'title': 'Profession', 'type': 'string'}, 
                            # 'is_employed': {'title': 'Is Employed', 'type': 'boolean'}, 
                            # 'years_of_experience': {'title': 'Years Of Experience', 'type': 'integer'}},
                            # 'required': ['profession', 'is_employed', 'years_of_experience'],
                            # 'title': 'CustomOutputSchema', 'type': 'object', 'additionalProperties': False}

# Validated JSON: {"profession":"Software Engineer","is_employed":false,"years_of_experience":5}