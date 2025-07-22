from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunContextWrapper, RunHooks
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

class TestHook(RunHooks):
    def __init__(self):
        self.event_counter = 0
        self.name = "Test Hook"

    async def on_agent_start(self, ctx:RunContextWrapper, agent: Agent)-> None:
        self.event_counter += 1
        print(f"{self.name} {self.event_counter}:\n{agent.name} Started!\nUsage: {ctx.usage}\n")
    
    async def on_agent_end(self, ctx:RunContextWrapper, agent:Agent, output: any) -> None:
        self.event_counter += 1
        print(f"{self.name} {self.event_counter}:\n{agent.name} Ended!\nUsage:{ctx.usage}\nOUTPUT:\n\n{output}")

# start_hook = TestHook()

start_agent = Agent(
    name="Content Moderator Agent",
    instructions="You are content moderation agent. Watch social media content received and flag queries that need help or answer. We will answer anything about AI?",
    model=model
)

async def main():
    await Runner.run(
        start_agent,
        input=f"Will Agentic AI Die at end of 2025?.",
        hooks = TestHook()
    )

asyncio.run(main())


# OUTPUT 👇🏻

# Test Hook 1:
# Content Moderator Agent Started!
# Usage: Usage(requests=0, input_tokens=0, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=0, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=0)

# Test Hook 2:
# Content Moderator Agent Ended!
# Usage:Usage(requests=1, input_tokens=43, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=333, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=1304)
# OUTPUT:

# That's a very interesting and speculative question!

# It's highly unlikely that Agentic AI will "die" by the end of 2025. Here's why:

# 1.  **Active Area of Research and Development:** Agentic AI, which refers to AI systems designed to act autonomously, plan, reason, and achieve goals, is currently one of the most active and promising areas of AI research. Major tech companies, academic institutions, and startups are heavily investing in it.
# 2.  **Evolution, Not Extinction:** In the world of technology, concepts rarely "die" completely, especially not within such a short timeframe. They typically evolve, merge with other technologies, or become integrated into broader systems. Agentic capabilities are seen as a crucial step towards more sophisticated and useful AI applications.
# 3.  **Foundation for Future AI:** The ability of AI to act as an "agent" – understanding context, planning steps, executing tasks, and even self-correcting – is considered fundamental to developing more advanced AI assistants, autonomous systems (like self-driving cars or robotic process automation), and even general artificial intelligence.
# 4.  **Early Stages:** While the concept has been around, the practical implementation and widespread adoption of highly capable agentic AI are still in relatively early stages. There's a lot of ongoing work to address challenges like reliability, safety, and scalability.

# Instead of "dying," it's far more probable that Agentic AI will continue to evolve rapidly, overcome current limitations, and find its way into an increasing number of real-world applications over the next few years.