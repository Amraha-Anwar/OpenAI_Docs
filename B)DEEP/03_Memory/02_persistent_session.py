from agents import Agent, Runner, SQLiteSession
from dotenv import load_dotenv
from rich import print

load_dotenv()

agent = Agent(
    name="Assistant",
    instructions = "You are a helpful assistant. Help user with their query and make sure to reply concisly ALWAYS.",
    model = 'gpt-4o-mini'
)

permanent_session = SQLiteSession("our_conversation", "text_chat.db")

while True:
    user_input = input("hey! How may I help you?\n")
    if user_input == "stop":
        break

    response = Runner.run_sync(
        agent,
        user_input,
        session = permanent_session
    )

    print(f"Agent: {response.final_output}")



# OUTPUT 👇🏻

# hey! How may I help you?
# hey I am Amraha and next week is my birthday:)

# Agent: Happy early birthday, Amraha! Do you have any special plans for your celebration?

# hey! How may I help you?
# ahh I forgot! when is my birthday do you remember?

# Agent: You mentioned it's next week, but I don’t have the exact date. When is it?

# hey! How may I help you?
# it's on 23 september wohoo 

# Agent: That's awesome! Just a few days away. Do you have any plans for your birthday celebration?

# hey! How may I help you?
# stop


# -------------- after terminating the block it still remembers the previous conversation ----------

# hey! How may I help you?
# when is my birthday?

# Agent: Your birthday is on September 23rd!