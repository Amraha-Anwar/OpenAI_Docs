from agents import (
        Agent,
        Runner,
        handoff,
        HandoffInputData,
        function_tool
)
from dotenv import load_dotenv
from rich import print
import asyncio

load_dotenv()

def summarize_billing_issues(data: HandoffInputData) -> HandoffInputData:
    print("\n\n[HANDOFF] Transferring to technical support...\n\n")
    summarized_issue = "User has a technical issue with their account."
    print("\nSummarized_issue:", data.input_history)
    print("\n\n[ITEM 2]", data.pre_handoff_items)
    print("\n\n[ITEM 1]", data.new_items)

# The corrected part: returns HandoffInputData with correct types
    return HandoffInputData(
        input_history=summarized_issue,
        pre_handoff_items=(),  # Corrected to an empty tuple
        new_items=(),         # Corrected to an empty tuple
)

@function_tool
async def get_user_account_status(user_id: str) -> str:
    """Gets the account status for a user."""
    return f"Account status for user {user_id} is active."

technical_support_agent: Agent = Agent(
    name="TechnicalSupportAgent",
    instructions="You are a technical support expert. You troubleshoot account and service issues for users.",
    model='gpt-4o-mini',
    tools=[get_user_account_status],
)

billing_agent: Agent = Agent(
    name="BillingAgent",
    instructions="You are a billing expert. You handle all payment and subscription questions. For any technical issues, you must hand off to the TechnicalSupportAgent.",
    model='gpt-4o-mini',
    tools=[get_user_account_status],
    handoffs=[handoff(agent=technical_support_agent, input_filter=summarize_billing_issues)]
)

initial_query = "My subscription payment went through, but my account is still showing as inactive."
result = Runner.run_sync(billing_agent, initial_query)

print("\nAGENT NAME", result.last_agent.name)
print("\n[FINAL RESPONSE]", result.final_output)