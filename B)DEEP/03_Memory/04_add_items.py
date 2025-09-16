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

new_items = [
    {"role": "user", "content": "ADD THIS ITEM"},
    {"role": "assistant", "content": "ITEM ADDED SUCCESSFULLY"}
]

async def main():
    await Session.add_items(new_items)
    user_data = await Session.get_items()
    for user in user_data:
        print(f"{user["role"]}: {user["content"]}")
    

asyncio.run(main())


# OUTPUT 👇🏻


# user: hey I am Amraha and next week is my birthday:)
# assistant: [{'annotations': [], 'text': 'Happy early birthday, Amraha! Do you have any special plans for your celebration?', 'type': 'output_text', 'logprobs': []}]
# user: ahh I forgot! when is my birthday do you remember?
# assistant: [{'annotations': [], 'text': "You mentioned it's next week, but I don’t have the exact date. When is it?", 'type': 'output_text', 'logprobs': []}]
# user: it's on 23 september wohoo
# user: ADD THIS ITEM
# assistant: ITEM ADDED SUCCESSFULLY
