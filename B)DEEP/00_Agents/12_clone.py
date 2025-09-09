from agents import Agent, Runner
from dotenv import load_dotenv
from rich import print


load_dotenv()

original_agent = Agent(
    name = "Main Agent",
    instructions = "Assistant that helps with various tasks.",
    model = "gpt-4o-mini",
)

copied_agent = original_agent.clone(
    name = "Cloned Agent",
)

result = Runner.run_sync(
        copied_agent,
        "Write a sweet birthday wish note for my childhood friend.",
    )
print(result.final_output)  
print(result.last_agent.name) 