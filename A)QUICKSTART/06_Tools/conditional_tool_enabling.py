from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

load_dotenv()

# @function_tool(is_enabled = True)
@function_tool(is_enabled = False)
def user_profile(status: int) -> str:
    """returns user's activity status.
    
    Args:
        status: user's activity status [active/inactive]
    """
    return f"Your Profile is curreently {status} due to some technical issues. We'll fix your problem shortly!"

agent = Agent(
    name = "Assistant",
    instructions = "you are a helful assistant, help user with their query"
    "if user talks about his/her profile related issue use tool [user_profile] to reply them."
    "don't reply by yourself.",
    model = 'gpt-4o-mini',
    tools = [user_profile]
)

result = Runner.run_sync(
    agent,
    "My profile is continuously inactive from past 2 days. What's the reason?"
)

print(result.final_output)


# OUTPUT when is_enabled = True 👇🏻
# Your profile is currently inactive due to some technical issues. We're working to resolve the problem shortly!


# OUTPUT when is_enabled = False 👇🏻
# I'm unable to access your profile details right now.