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
        
    def validate_json(self, json_str:str) -> any:
        return json_str
    
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

    print(result.final_output)

asyncio.run(main())

# OUTPUT👇🏻

# {"profession":"Software Engineer","is_employed":false,"years_of_experience":5}