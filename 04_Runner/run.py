from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    RunConfig
)
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
url = os.getenv("BASE_URL")

if not gemini_api_key or not url:
    raise ValueError("GEMINI_API_KEY and BASE_URL must be set")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=url,
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-exp",
    openai_client=client,
)

config = RunConfig(
    model= model,
    model_provider=client,
    tracing_disabled=True,
)

agent = Agent(
    name = "Gemini Agent",
    instructions = "You are a helpful assistant that can answer questions and help with tasks.",
    model = model,
)

async def main():
    result = await Runner.run(agent, "what is meant by the term 'AI'?", run_config=config)
    # print(result.last_agent)
    # print(result.final_output)
    # print(result)
    # print(result.input)
    print(result.raw_responses)



if __name__ == "__main__":
    asyncio.run(main())


# OUTPUT 👇🏻

# RunResult:
# - Last agent: Agent(name="Gemini Agent", ...)
# - Final output (str):
#     The term "AI" stands for **Artificial Intelligence**.
    
#     In broad terms, AI refers to the ability of a computer or machine to mimic human cognitive functions such as:
    
#     *   **Learning:** Acquiring information and rules for using the information.
#     *   **Reasoning:** Using rules to reach conclusions (either definite or approximate).
#     *   **Problem-solving:** Devising strategies to overcome difficulties.
#     *   **Perception:** Using sensors to deduce aspects of the world.
#     *   **Understanding natural language:** Processing and understanding human languages (like English or Spanish).
    
#     Essentially, AI aims to create systems that can perform tasks that typically require human intelligence.
# - 1 new item(s)
# - 1 raw response(s)
# - 0 input guardrail result(s)
# - 0 output guardrail result(s)
# (See `RunResult` for more details)