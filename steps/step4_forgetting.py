"""
Step 4: the list is the memory, and memory has a size limit.
This is step 2 again, plus six lines that throw the oldest turns away
once the conversation grows past a budget. Watch it forget, live.
"""

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

BUDGET = 60   # tokens, small on purpose; lower it to forget sooner


def n_tokens(messages):
    """Roughly how big the conversation is, in tokens."""
    # Written English averages about four letters per token. Counting letters
    # and dividing by four is not exact, but it is plenty for a budget.
    letters = 0
    for message in messages:
        letters += len(message["content"])
    return letters // 4


def fit(messages, budget=BUDGET):
    system, rest = messages[0], messages[1:]
    while n_tokens([system] + rest) > budget and len(rest) > 2:
        rest = rest[2:]          # drop the oldest user + assistant pair
        print("[context: older turns dropped]")
    return [system] + rest


messages = [{"role": "system", "content": "Answer in two or three sentences."}]
while True:
    messages.append({"role": "user", "content": input("you> ")})
    # The list here is nothing but user and assistant taking turns, so
    # removing two entries always removes one complete exchange.
    messages = fit(messages)
    reply = client.chat.completions.create(model="gemma4:e2b", messages=messages)
    answer = reply.choices[0].message.content
    print("bot>", answer)
    messages.append({"role": "assistant", "content": answer})
    print("[" + str(n_tokens(messages)) + " tokens in memory]")
