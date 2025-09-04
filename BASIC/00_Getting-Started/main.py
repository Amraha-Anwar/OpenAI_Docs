from agents import Agent, AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled, Runner
from dotenv import load_dotenv
import asyncio
import os


load_dotenv()
set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")
url = os.getenv("BASE_URL")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=url,
    )

model= OpenAIChatCompletionsModel(
    model = 'gemini-2.0-flash',
    openai_client = external_client,
)


history_tutor_agent = Agent(
    name = "History Tutor",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
    handoff_description = "Specialist Agwnt for Historical questions.",
    model = model,
)

math_tutor_agent = Agent(
    name = "Math Tutor",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
    handoff_description = "Specialist Agent for Math questions.",
    model = model,
)

triage_agent = Agent(
    name = "Triage Agent",
    instructions = "You determine which agent to use based on user's homework question",
    model = model,
    handoffs = [history_tutor_agent, math_tutor_agent],
)

async def main():
    result = await Runner.run(triage_agent, "who was the first president of the united states?")
    print(result.final_output)

    result = await Runner.run(triage_agent, "what is life")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())




# OUTPUT 👇🏻
# The first president of the United States was **George Washington**. He served from 1789 to 1797.

# Here's some important context:

# *   **Leading the Continental Army:** Before becoming president, Washington was the Commander-in-Chief of the Continental Army during the American Revolutionary War (1775-1783). His leadership was crucial in securing independence from Great Britain.
# *   **Constitutional Convention:** After the war, Washington presided over the Constitutional Convention of 1787. This convention drafted the U.S. Constitution, which established a new form of government.
# *   **Unanimous Election:** Washington was unanimously elected as the first president by the Electoral College in 1789. This reflects the high esteem and trust he held among the founding fathers.
# *   **Setting Precedents:** As the first president, Washington set many important precedents for future presidents. These included:

#     *   Forming a cabinet of advisors.
#     *   Serving only two terms (he voluntarily stepped down after two terms, establishing a norm that was followed until Franklin D. Roosevelt).
#     *   Maintaining neutrality in foreign affairs (particularly during the French Revolution).
# *   **Challenges During his Presidency:** Some of the major challenges during his presidency included:

#     *   Establishing the authority and legitimacy of the new federal government.
#     *   Dealing with the Whiskey Rebellion (a tax revolt in western Pennsylvania).
#     *   Navigating complex foreign policy issues.

# Washington is widely considered one of the most important figures in American history due to his leadership during the Revolution and his role in shaping the early years of the United States.

# I am not equipped to handle philosophical questions. I can transfer you to a specialized agent for either history or math questions.
