from agents import Agent, Runner, SQLiteSession
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    name = "Assistant Agent",
    instructions="Help user with their Query. Reply very concisely.",
    model = 'gpt-4o-mini'
)

session = SQLiteSession("my_session", "our_conversation.db")

while True:
    user_input = input("Ask Ahead: ")

    if user_input == "stop":
        break

    response = Runner.run_sync(
        agent,
        user_input,
        session = session
    )

    print(response.final_output)


# OUTPUT 👇🏻

# ⌨️ uv run with_database.py
# Ask Ahead: hey! I'm Amraha
# Hi Amraha! How can I help you today?
# Ask Ahead: who am I?
# You’re Amraha! If you’re looking for something specific about yourself, feel free to share.
# Ask Ahead: stop

# ⌨️ uv run with_database.py
# Ask Ahead: what is my name?
# Your name is Amraha.


## NOTE 📌
# Now it will save my information in that our_conversation.db memory even after terminating the conversation