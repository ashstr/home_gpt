# home_gpt

A tiny chat assistant that runs entirely on your own machine.

## Setup

```
./setup.sh                 # Mac: or just double-click setup.command
source .venv/bin/activate
python chat.py
```

`setup.sh` installs Ollama if you don't have it, creates a `.venv` with the one
package this needs, and downloads the model (a few GB, once). Running it again
is harmless — it skips whatever is already there.

By hand instead: install [Ollama](https://ollama.com), `ollama pull gemma4:e2b`,
`pip install -r requirements.txt`, `python chat.py`.

`HOME_GPT_MODEL` switches the model `chat.py` uses; the steps name it inline.

## The demo, in order

Each step adds one idea. The steps are standalone and repeat a few lines on
purpose, so any one of them fits on a slide.

1. `python steps/step1_one_call.py` — one call in, one answer out.
2. `python steps/step2_chat.py` — the same thing, streaming. Ask a follow-up
   ("and in French?") to show that the list of messages, not the model, is
   what carries the conversation.
3. `python steps/step3_one_tool.py` — one question, two trips to the model.
   It asks for the clock, *we* read it, and only then can it answer.
4. `python steps/step4_forgetting.py` — ask three throwaway questions, then
   *"What was my first question?"*. On the fourth turn `[context: older turns
   dropped]` appears and the answer is confidently wrong: that turn is gone.
5. `python chat.py` — all of it together, with three tools:
   - *"What time is it in Amsterdam?"* — watch the `[tool]` line.
   - *"Remember that I prefer short answers."*, quit, restart, then *"What do
     you know about me?"* — the memory is a file, not something it learned.

Two things depend on the model, so rehearse with the one you will use:
whether a tool fires at all, and how many turns step 4 takes to start
forgetting (raise or lower its `BUDGET`).

## Break it on purpose

- Delete a tool's `description` in `tools.py` and ask for the time. The model
  no longer knows what the tool is for, so it guesses instead.
- Shorten `recall`'s description to "Read the notes." and ask what it knows
  about you. It stops bothering to look and just says it has no idea.
- Set `MAX_ROUNDS = 1` in `chat.py`. The model gets its tool result but has no
  turn left to say anything about it.
