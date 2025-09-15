from agents import Agent, Runner, SQLiteSession
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    name = "Assistant Agent",
    instructions="Help user with their Query. Reply very concisely.",
    model = 'gpt-4o-mini'
)

session = SQLiteSession("my_session")

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

# Ask Ahead: hello I'm Amraha
# Hi Amraha! How can I help you today?
# Ask Ahead: who am I?
# You’re Amraha! If you’d like to share more about yourself, feel free!
# Ask Ahead: stop


## NOTE 📌
# But when we terminate the conversation, it will completely forget about our previous chat history