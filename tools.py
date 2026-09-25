"""
What the model is allowed to ask for, and the plain Python that actually does it.
Three small jobs: tell the time, write a note down, read the notes back.
"""

import json
from datetime import datetime
from zoneinfo import ZoneInfo

NOTES = "notes.txt"


def get_time(tz):
    """The current time in a city's timezone, like 'Friday 14:02'."""
    return datetime.now(ZoneInfo(tz)).strftime("%A %H:%M")


def remember(text):
    """Write one line into the notes file."""
    with open(NOTES, "a") as notes:
        notes.write(text + "\n")
    return "Saved."


def recall():
    """Read back everything we have written down so far."""
    try:
        with open(NOTES) as notes:
            return notes.read().strip() or "No notes yet."
    except FileNotFoundError:
        return "No notes yet."


# The model picks a tool by reading these descriptions, so they say, briefly
# and specifically, when each tool applies.
SCHEMAS = [
    {"type": "function", "function": {"name": "get_time",
        "description": "Current time in a timezone such as Europe/Amsterdam. Use for any question about the time.",
        "parameters": {"type": "object", "properties": {"tz": {"type": "string"}}, "required": ["tz"]}}},
    {"type": "function", "function": {"name": "remember",
        "description": "Save a fact about the user. Use it whenever the user says to remember something.",
        "parameters": {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]}}},
    {"type": "function", "function": {"name": "recall",
        "description": "Read the saved notes about the user. Call this before answering "
                       "anything about the user, what they like, or what they told you earlier.",
        "parameters": {"type": "object", "properties": {}}}},
]

# The point of this file: the model never runs anything. It asks; we decide.
DISPATCH = {"get_time": get_time, "remember": remember, "recall": recall}


def run(name, arguments_json):
    """Carry out one tool request and always hand back a string."""
    # A mistake here is not fatal. Given a sentence explaining what went wrong,
    # the model can usually try again. A program that crashed cannot.
    function = DISPATCH.get(name)
    if function is None:
        return "There is no tool called " + name + "."
    try:
        arguments = json.loads(arguments_json or "{}")
        return str(function(**arguments))
    except Exception as problem:
        return "That tool call did not work: " + str(problem)
