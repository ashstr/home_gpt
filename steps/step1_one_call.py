"""
Step 1: the smallest thing that works.
One question, one answer, and then the program ends.
"""

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
answer = client.chat.completions.create(
    model="gemma4:e2b",
    messages=[{"role": "user", "content": "In one sentence: what is a token?"}],
)
print(answer.choices[0].message.content)
