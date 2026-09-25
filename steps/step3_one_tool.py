"""
Step 3: the whole tool-call dance, once, with nothing else around it.
The model asks for a tool, our code runs it, the result goes back,
and only then can the model answer. One question, two trips to the model.
"""

import json
from datetime import datetime
from zoneinfo import ZoneInfo

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


def get_time(tz):
    return datetime.now(ZoneInfo(tz)).strftime("%A %H:%M")


# This description is everything the model knows about our tool.
# It decides whether to use it by reading these words.
schema = {"type": "function", "function": {"name": "get_time",
    "description": "Current time in a timezone such as Europe/Amsterdam.",
    "parameters": {"type": "object",
                   "properties": {"tz": {"type": "string"}},
                   "required": ["tz"]}}}

messages = [{"role": "user", "content": "What time is it in Amsterdam?"}]

# First trip. The model has no clock, so it asks for one.
reply = client.chat.completions.create(
    model="gemma4:e2b", messages=messages, tools=[schema]).choices[0].message

if not reply.tool_calls:
    print("bot>", reply.content)   # it decided it could answer on its own
    raise SystemExit

call = reply.tool_calls[0]
print("the model asked for:", call.function.name, call.function.arguments)

# Our code runs it. The model never runs anything; it only asks.
result = get_time(**json.loads(call.function.arguments))
print("we answered:", result)

messages.append(reply)                                     # what it asked for
messages.append({"role": "tool",                           # what we told it
                 "tool_call_id": call.id,
                 "content": result})

# Second trip. Same question, but now the clock reading is in the conversation.
answer = client.chat.completions.create(
    model="gemma4:e2b", messages=messages).choices[0].message
print("bot>", answer.content)
