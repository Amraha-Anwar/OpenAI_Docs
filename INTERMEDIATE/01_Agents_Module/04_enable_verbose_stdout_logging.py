from agents import Agent, Runner, enable_verbose_stdout_logging
from dotenv import load_dotenv
import os

load_dotenv()
enable_verbose_stdout_logging()

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model = 'gpt-4o-mini',
)

result = Runner.run_sync(
    agent,
    "helloooo"
)

print(result.final_output)


# OUTPUT 👇🏻


# Creating trace Agent workflow with id trace_ff441b3c385d4bb3b44b9ab9c57d0a4b
# Setting current trace: trace_ff441b3c385d4bb3b44b9ab9c57d0a4b
# Creating span <agents.tracing.span_data.AgentSpanData object at 0x0000014DEA02DB80> with id None
# Running agent Assistant (turn 1)
# Creating span <agents.tracing.span_data.ResponseSpanData object at 0x0000014DE85C0FD0> with id None
# Calling LLM gpt-4o-mini with input:
# [
#   {
#     "content": "helloooo",
#     "role": "user"
#   }
# ]
# Tools:
# []
# Stream: False
# Tool choice: NOT_GIVEN
# Response format: NOT_GIVEN
# Previous response id: None
# Conversation id: None

# LLM resp:
# [
#   {
#     "id": "msg_68c081b4ec24819d99b80da24aa0b7360895abcd06741da7",
#     "content": [
#       {
#         "annotations": [],
#         "text": "Hello! How can I assist you today?",
#         "type": "output_text",
#         "logprobs": []
#       }
#     ],
#     "role": "assistant",
#     "status": "completed",
#     "type": "message"
#   }
# ]

# Resetting current trace
# Hello! How can I assist you today?
# Shutting down trace provider
# Shutting down trace processor <agents.tracing.processors.BatchTraceProcessor object at 0x0000014DE85F2720>
# Exported 3 items