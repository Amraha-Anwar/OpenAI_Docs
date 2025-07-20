from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunContextWrapper, AgentHooks
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
set_tracing_disabled(True)
gemini_api_key = os.getenv("GEMINI_API_KEY")
url = os.getenv("BASE_URL")
MODEL = 'gemini-2.5-flash'

client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url = url
)

model = OpenAIChatCompletionsModel(
    model = MODEL,
    openai_client = client
)

class AnAgent(AgentHooks):
    def __init__(self, agent_name):
        self.event_counter = 0
        self.agent_name = agent_name

    async def on_start(self, context:RunContextWrapper, agent:Agent) -> None:
        self.event_counter += 1
        print(f"\n{self.agent_name} {self.event_counter}:\n{agent.name} Agent Started!"
              f"\nUsage: {context.usage}")
            
    async def on_end(self, context:RunContextWrapper, agent:Agent, output: any) -> None:
        self.event_counter += 1
        print(f"\n{self.agent_name} {self.event_counter}:\n{agent.name} Agent Ended!"
              f"\nUsage: {context.usage}"
              f"\nOUTPUT:\n\n{output}")
            
agent = Agent(
    name = "LinkedIn Post Maker",
    instructions = "You are a post maker for LinkedIn, take topic from user's input text and write a not so long professional post on that topic.",
    model = model,
    hooks = AnAgent(agent_name="LinkedIn Post Maker")
)

async def main():
    result = await Runner.run(
        agent,
        "Write a LinkedIn post for me on 'future of AI'."
    )

    # print(result.final_output)          

asyncio.run(main())


# OUTPUT👇🏻

# LinkedIn Post Maker 1:
# LinkedIn Post Maker Agent Started!
# PROMPT TOKEN: 0
# RESPONSE TOKEN: 0
# TOTAL TOKENS: 0

# LinkedIn Post Maker 2:
# LinkedIn Post Maker Agent Ended!
# PROMPT TOKEN: 42
# RESPONSE TOKEN: 189
# TOTAL TOKENS: 231
# OUTPUT:

# Here's a professional and concise LinkedIn post about the future of AI:

# The future of AI isn't just a distant concept; it's unfolding right before our eyes, promising to redefine industries, roles, and how we interact with technology.

# Rather than just automation, we're seeing a shift towards powerful human-AI synergy. Imagine AI as an intelligent co-pilot, augmenting our capabilities and unlocking new levels of creativity and efficiency. This isn't about replacing human ingenuity, but amplifying it.

# Of course, this journey comes with crucial conversations around ethics, transparency, and responsible development. Navigating these complexities will be key to harnessing AI's full potential for good.

# The era of augmentation is here. How do you see AI shaping your industry or role in the next decade? Share your thoughts! 👇

#AI #FutureOfWork #Innovation #ArtificialIntelligence #TechForGood #DigitalTransformation