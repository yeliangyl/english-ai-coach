#!/bin/bash
set -e

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  echo "Virtual environment not found. Run ./setup_macos.sh first."
  exit 1
fi

if [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "OPENAI_API_KEY is not set."
  echo 'For this Terminal session, run: export OPENAI_API_KEY="your_api_key_here"'
  exit 1
fi

source .venv/bin/activate
python -m streamlit run app.py
