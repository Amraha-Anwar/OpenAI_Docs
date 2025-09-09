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
# Usage: Usage(requests=0, input_tokens=0, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=0, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=0)

# LinkedIn Post Maker 2:
# LinkedIn Post Maker Agent Ended!
# Usage: Usage(requests=1, input_tokens=42, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=220, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=1258)
# OUTPUT:

# Here's a professional LinkedIn post about the future of AI:

# ---

# 💡 The "future of AI" isn't some distant concept; it's unfolding at an unprecedented pace, transforming how we live and work.

# It's increasingly clear that AI's greatest potential lies not in replacing human intellect, but in **augmenting** it. Imagine enhanced creativity, accelerated problem-solving, and entirely new ways of collaborating. From hyper-personalized experiences to breakthroughs in scientific research and sustainable solutions, AI is poised to redefine what's possible across every industry.

# However, this future also demands our mindful attention to ethics, transparency, and inclusivity. Responsible development isn't just a buzzword; it's the foundation for a beneficial AI-powered world.

# How do you envision AI shaping your industry or role in the coming years? What skills do you believe will be most crucial for thriving in an AI-integrated future?

# Let's discuss! 👇

#AI #ArtificialIntelligence #FutureOfWork #Innovation #TechTrends #DigitalTransformation #HumanAICollaboration