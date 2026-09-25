"""
The only file that talks to the language model.
Everything else in this project goes through the three functions below:
ask (say something), warm_up (wake the model), clean (tidy the answer).
"""

import os
import re

from openai import OpenAI

# Ollama runs on this machine and speaks the same dialect as OpenAI,
# so the official library works unchanged. The key is ignored, but required.
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

MODEL = os.environ.get("HOME_GPT_MODEL", "gemma4:e2b")


def ask(messages, tools=None):
    """Send the whole conversation, get one message back."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
    )
    return response.choices[0].message


def warm_up():
    """Load the model into memory before anyone is watching."""
    # The first call to a cold model can take many seconds while it is read
    # from disk. We spend that wait here, and ask for one token we throw away.
    try:
        ask_once = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=1,
        )
        return ask_once is not None
    except Exception:
        return False


def clean(text):
    """Remove the model's private thinking and any stray whitespace."""
    # Some models think out loud first and wrap those notes in <think> tags.
    # That is scratch work, not an answer, so it never reaches the screen.
    without_thoughts = re.sub(r"<think>.*?</think>", "", text or "", flags=re.DOTALL)
    return without_thoughts.strip()
