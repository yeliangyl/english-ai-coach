#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "Setting up English AI Coach for macOS..."

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 was not found."
  echo "Install Python 3 from https://www.python.org/downloads/macos/ and run this script again."
  exit 1
fi

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo
echo "Setup complete."
echo "Before starting the app, set OPENAI_API_KEY in your terminal or shell profile."
echo "Then run: ./start_macos.sh"
