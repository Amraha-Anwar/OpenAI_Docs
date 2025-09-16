from agents import Agent, Runner, SQLiteSession
from dotenv import load_dotenv
from rich import print

load_dotenv()

agent = Agent(
    name="Personal Assistant",
    instructions="You are a personal assistant of the user. Provide your best assistance service.",
    model = 'gpt-4o-mini'
)

session = SQLiteSession("our_conversation")

print("\n======= Agent's First Response ========\n")

response1 = Runner.run_sync(
    agent,
    "Hey Assistant! I am Amraha & I love reading books :)",
    session = session
)

print(f"First response: {response1.final_output}\n")

print("======= Agent's Second Response ========\n")

response2 = Runner.run_sync(
    agent,
    "Who am I and what do I love to do?",
    session = session
)

print(f"Second Response: {response2.final_output}\n")


# OUTPUT 👇🏻

# ======= Agent's First Response ======== 

# First response: Hi Amraha! It’s great to meet a fellow book lover! What genres or authors do you enjoy the most? Are you 
# looking for any recommendations or discussing a specific book?

# ======= Agent's Second Response ======== 

# Second Response: You’re Amraha, and you love reading books! If there’s anything specific you’d like to explore about your 
# interests or books in general, feel free to share!
