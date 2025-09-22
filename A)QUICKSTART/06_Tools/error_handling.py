from agents import Agent, Runner, function_tool, RunContextWrapper
from dotenv import load_dotenv

load_dotenv()

def custom_error_func(ctx: RunContextWrapper, error: Exception) -> str:
    """ A function to provide user-friendly error messages."""
    print(f"A tool called failed with the error:\n{error}")
    return "An internal server error occured. Please try again later."  #this message will be sent to LLM


@function_tool(failure_error_function=custom_error_func)
def get_user_info(id: str) -> str:
    """Fetching user's info from mock API
    This function demonstrate a failure of an API call.
    """
    if id == "user_123":
        return f"User profile for 'user_123' successfully retrieved."
    else:
        raise ValueError(f"Could not retrieved profile for user_id: {id}. API returned an error.")
    

agent = Agent(
    name = "Assistant Agent",
    instructions = "You are a helpful Assistant. If user wants to retrieve his/her profile, must use tool [get_user_info].",
    model = 'gpt-4o-mini',
    tools = [get_user_info]
)

result = Runner.run_sync(
    agent,
    "I wanna retrieve my profile. My id is 'user_1'."
)
print(result.final_output)


# OUTPUT👇🏻

# A tool called failed with the error:
# Could not retrieved profile for user_id: user_1. API returned an error.

# It seems there was an internal server error while trying to retrieve your profile.
# Please try again later or check if there's an issue on the platform. 
# If you have any other questions or need assistance with something else, feel free to ask!