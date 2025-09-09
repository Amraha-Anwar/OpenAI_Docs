from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, Runner, RunContextWrapper, function_tool
from dataclasses import dataclass
from dotenv import load_dotenv
# import asyncio
import os 

load_dotenv()
set_tracing_disabled(disabled = True)

gemini = os.getenv("GEMINI_API_KEY")
url = os.getenv("BASE_URL")

client = AsyncOpenAI(
    api_key= gemini,
    base_url= url
)

model = OpenAIChatCompletionsModel(
    model = 'gemini-2.0-flash',
    openai_client = client
)

@dataclass
class UserInfo:
    name: str
    id: int

@function_tool
async def get_user_data(wrapper:RunContextWrapper[UserInfo]) -> str:
    """Return User's Name and ID"""
    return f"User Name: {wrapper.context.name}\nUser ID: {wrapper.context.id}"

user_info = UserInfo(name = "Amraha", id = 2301)

agent = Agent[UserInfo](
    name = "Agent",
    instructions = "You are a helpful assistant.",
    model = model,
    tools = [get_user_data]
)

input = input("Ask me Anything...")
result = Runner.run_sync(
    agent,
    input = input,
    context = user_info
)

print(result)


# OUTPUT 👇🏻
# Ask me Anything...user name and id?
# RunResult:
# - Last agent: Agent(name="Agent", ...)
# - Final output (str):
#     User Name: Amraha
#     User ID: 2301
# - 3 new item(s)
# - 2 raw response(s)
# - 0 input guardrail result(s)
# - 0 output guardrail result(s)