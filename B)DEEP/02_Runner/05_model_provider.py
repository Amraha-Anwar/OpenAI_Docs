from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig,
    Runner
)
from dotenv import load_dotenv
import os

load_dotenv()

# { ------------------ DEFAULTS TO OPENAI ------------------ 
gemini_api_key = os.getenv("GEMINI_API_KEY")
url = os.getenv("BASE_URL")

gemini_api_key = os.getenv("GEMINI_API_KEY")
url = os.getenv("BASE_URL")

external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url = url
)

model = OpenAIChatCompletionsModel(
    model= 'gemini-2.5-flash',
    openai_client = external_client
)

config = RunConfig(
    model = model,
    model_provider = external_client,    #Responses API with OPENAI KEY
    tracing_disabled = True
)

# } ------------------ DEFAULTS TO OPENAI ------------------ 

agent = Agent(
    name = "Assitant",
    instructions = "solve user's queries."
)

result = Runner.run_sync(
    agent,
    "hello! This is Amraha!",
    run_config = config
)

print(result.final_output)