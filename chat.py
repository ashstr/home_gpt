"""
The whole assistant, in one loop: a question goes in, the model asks for a
tool, our code runs it, the result goes back, and the model answers.
Run it with: python chat.py
"""

import sys

from llm import MODEL, ask, clean, warm_up
from tools import SCHEMAS, run

SYSTEM = {"role": "system", "content": (
    "You are a small local assistant. Answer in at most three sentences. "
    "Never guess the time or what you were told before: use your tools. "
    "When you are asked to remember something, save it with a tool."
)}

# Without a cap, a confused model can ask for tools forever.
MAX_ROUNDS = 5


def answer_turn(messages):
    """Let the model use tools until it has a sentence for us."""
    for _ in range(MAX_ROUNDS):
        reply = ask(messages, SCHEMAS)
        if not reply.tool_calls:
            answer = clean(reply.content)
            print("bot> " + answer)
            messages.append({"role": "assistant", "content": answer})
            return
        # The model's request has to go in before the answers to it.
        messages.append(reply)
        for call in reply.tool_calls:
            result = run(call.function.name, call.function.arguments)
            print("[tool] " + call.function.name + "(" + call.function.arguments + ") -> " + result)
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
    print("[stopped after " + str(MAX_ROUNDS) + " tool rounds]")


def main():
    if not warm_up():
        print("No model answered. Start it first with: ollama serve")
        sys.exit(1)
    print("home_gpt is using " + MODEL + ". Press enter on an empty line to quit.")

    # One list holds the whole conversation: our questions, the model's
    # answers, every tool it asked for and every result we handed back.
    messages = [SYSTEM]
    while True:
        try:
            question = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not question:
            break
        messages.append({"role": "user", "content": question})
        answer_turn(messages)


main()
