from agents import Agent, Runner, function_tool, FunctionToolResult, ToolsToFinalOutputResult, RunContextWrapper
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio

load_dotenv()


class Student(BaseModel):
    name : str
    grade: int
    subjects: list[str]

@function_tool
def get_student_details(ctx: RunContextWrapper[Student]) -> str:
    """returns the details of the Student"""
    return f"\nName: {ctx.context.name}\nGrade: {ctx.context.grade}\nSubjects: {ctx.context.subjects}."


def custom_output_func(ctx: RunContextWrapper, result:list[FunctionToolResult]) -> ToolsToFinalOutputResult:
    print("---custom output---")
    return ToolsToFinalOutputResult(
        is_final_output = True,
        final_output = "This is a custom final output"
    )


std_details = Student(name = "Amraha", grade = 9, subjects = ["Computer Science", "English", "Maths"])

agent = Agent(
    name = "Receptionist",
    instructions = "You are a school receptionist. Help clients with their query"
    "If user wants to know about the student. You must have to use the tool [get_student_details] for the information."
    "Don't respond with the wrong information by yourself.",
    model = 'gpt-4o-mini',
    tools= [get_student_details],
    tool_use_behavior = custom_output_func
)

async def main():
    result = await Runner.run(
        agent,
        "Tell me the details of student whose name is 'Amraha'.",
        context = std_details
    )

    print(result.final_output)

asyncio.run(main())


# REGULAR OUTPUT 👇🏻

# The details of the student Amraha are as follows:

# - **Grade:** 9
# - **Subjects:** Computer Science, English, Maths.


# OUTPUT by setting FuntionToolResult as a final output 👇🏻
# ---custom output---
# This is a custom final output