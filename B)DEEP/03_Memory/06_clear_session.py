from agents import Agent, Runner, SQLiteSession
from dotenv import load_dotenv
import asyncio

load_dotenv()

agent = Agent(
    name="Assistant",
    instructions = "You are a helpful assistant. Help user with their query and make sure to reply concisly ALWAYS.",
    model = 'gpt-4o-mini'
)

Session = SQLiteSession("our_conversation", "text_chat.db")

async def main():
    await Session.clear_session()
    user_data = await Session.get_items()
    print(user_data)
    

asyncio.run(main())


# OUTPUT 👇🏻

# []