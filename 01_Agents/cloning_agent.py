from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled ,Runner
import os
from dotenv import load_dotenv

load_dotenv()
set_tracing_disabled(disabled = True)

gemini_api_key = os.getenv("GEMINI_API_KEY")
url = os.getenv("BASE_URl")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=url,
)

model = OpenAIChatCompletionsModel(
    model = 'gemini-2.0-flash',
    openai_client = external_client,
)



original_agent = Agent(
    name = "Assistant Agent",
    instructions = "Help user with their query",
    model = model,
)

copied_one = original_agent.clone()


result = Runner.run_sync(copied_one,"3 benefits of Mango")
print(result.final_output)


# OUTPUT👇🏻
# Okay, here are three benefits of mangoes:

# 1.  **Rich in Vitamins and Antioxidants:** Mangoes are an excellent source of Vitamin C, which is crucial for immune function, collagen production, and skin health. They also contain other vitamins like Vitamin A (important for vision) and antioxidants like quercetin and beta-carotene, which help protect your cells from damage caused by free radicals.
# 2.  **May Improve Digestion:** Mangoes contain amylase enzymes that help break down complex carbohydrates, making them easier to digest. They also provide dietary fiber, which aids in promoting regular bowel movements and preventing constipation.
# 3.  **Good for Eye Health:** The Vitamin A and antioxidants like zeaxanthin and lutein found in mangoes contribute to good vision and can help protect the eyes from age-related macular degeneration and cataracts.
