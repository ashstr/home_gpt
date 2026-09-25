#!/bin/bash
# ============================================================================
#  home_gpt — one-time setup.
#
#  Installs what the demo needs and downloads the AI model:
#    - Python 3.10+
#    - Ollama (the thing that runs the model on your own machine)
#    - the one Python package we use (openai)
#    - the model itself (a few GB — this is the slow part)
#
#  Safe to run more than once: it skips whatever is already there.
#  Run it with:   ./setup.sh
# ============================================================================
cd "$(dirname "$0")" || exit 1

MODEL="${HOME_GPT_MODEL:-gemma4:e2b}"

have() { command -v "$1" >/dev/null 2>&1; }

# --- 1. Python 3.10+ --------------------------------------------------------
PYTHON=""
for candidate in python3 python3.13 python3.12 python3.11 python3.10; do
  if have "$candidate" && "$candidate" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)' 2>/dev/null; then
    PYTHON="$candidate"; break
  fi
done
if [ -z "$PYTHON" ]; then
  echo "Python 3.10 or newer is needed."
  have brew && echo "Try: brew install python@3.12" || echo "Get it from https://www.python.org/downloads/"
  exit 1
fi
echo "Python: $("$PYTHON" --version)"

# --- 2. Ollama --------------------------------------------------------------
if ! have ollama; then
  echo "Ollama is not installed."
  if have brew; then
    echo "Installing it with Homebrew..."
    brew install --cask ollama
    hash -r
  fi
fi
if ! have ollama; then
  echo
  echo "Please install Ollama, then run this script again:"
  echo "  Mac/Windows:  https://ollama.com/download"
  echo "  Linux:        curl -fsSL https://ollama.com/install.sh | sh"
  exit 1
fi
echo "Ollama: $(ollama --version 2>/dev/null | head -n 1)"

# --- 3. The Python package --------------------------------------------------
# A .venv folder keeps this project's package out of your system Python.
if [ ! -x ".venv/bin/python" ]; then
  echo "Creating .venv and installing the openai package..."
  "$PYTHON" -m venv .venv || { echo "Could not create the .venv folder."; exit 1; }
  ./.venv/bin/python -m pip install --upgrade pip -q
fi
./.venv/bin/python -m pip install -q -r requirements.txt \
  || { echo "Install failed — check your internet connection and try again."; exit 1; }

# --- 4. The model -----------------------------------------------------------
# Ollama needs to be running before it can download or serve anything.
if ! curl -s --max-time 3 localhost:11434/api/tags >/dev/null 2>&1; then
  echo "Starting Ollama in the background..."
  ollama serve >/dev/null 2>&1 &
  sleep 2
fi
if ollama list 2>/dev/null | grep -q "^$MODEL"; then
  echo "Model: $MODEL is already here."
else
  echo "Downloading $MODEL — a few GB, one time only. Please wait..."
  ollama pull "$MODEL" || { echo "Download failed. Check your connection and run this again."; exit 1; }
fi

echo
echo "=============================================="
echo " All set. Start the assistant with:"
echo
echo "   source .venv/bin/activate"
echo "   python chat.py"
echo "=============================================="
