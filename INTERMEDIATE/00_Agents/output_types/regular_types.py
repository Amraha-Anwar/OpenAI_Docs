from agents import (
    Agent,
    Runner,
)
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class StudentMarks(BaseModel):
    eng: int
    maths: int
    chem: int

class Student(BaseModel):
    name: str
    age: int
    roll_no : int
    marks : StudentMarks

agent = Agent(
    name= "StudentInfoAgent",
    instructions = "Extract and provide the exact student information from the input text.",
    model = 'gpt-4o-mini',
    output_type = Student,
)

result = Runner.run_sync(
    agent,
    "The student's name is Amraha, she is 20 years old and her roll number is 1011. She scored 85 in English, 90 in Mathematics, and 88 in Chemistry. Make a report with this information.",
)

print(result.final_output)