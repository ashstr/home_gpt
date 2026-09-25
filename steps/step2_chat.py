"""
Step 2: a conversation, printed word by word as the model writes it.
The list called messages is the only memory there is.
"""

from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
messages = [{"role": "system", "content": "You are terse."}]
while True:
    messages.append({"role": "user", "content": input("you> ")})
    stream = client.chat.completions.create(
        model="gemma4:e2b", messages=messages, stream=True)
    reply = ""
    for chunk in stream:
        piece = chunk.choices[0].delta.content or ""
        print(piece, end="", flush=True)
        reply += piece
    print()
    messages.append({"role": "assistant", "content": reply})
