from agents import Agent, Runner, ModelSettings, function_tool
from dotenv import load_dotenv

load_dotenv()

@function_tool(is_enabled = True)
def story_generator(topic: str) -> str:
    """Generates a short story on given topic
    
    Args
        topic: topic, the story will be genrated on
    """
    return f"Your story on {topic} is ready. I'll print it shortly."

agent = Agent(
    name = "Story teller",
    instructions = "You are a story teller. If user asks for the story on any topic, you must have to use the tool"
    "If the tool is not available, do apologies but Don't generate the story by yourself.",
    model = 'gpt-4o-mini',
    tools = [story_generator],
    model_settings = ModelSettings(
        tool_choice = 'required'
    )
)

response = Runner.run_sync(
    agent,
    "Generate a story on 'A lion King'."
)

print(response.final_output)