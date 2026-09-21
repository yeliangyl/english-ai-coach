# English AI Coach

A voice-first English speaking practice app built with Streamlit and the OpenAI API. The coach starts the conversation, listens to your answer, gives focused corrections, provides natural spoken English feedback, rewrites your answer as a better version, and asks one follow-up question.

## Features

- Voice or typed answers
- Speech-to-text transcription
- Focused grammar corrections with concise Chinese explanations
- More natural English alternatives
- Spoken English coaching feedback plus text
- A polished **Better Version** with text and TTS playback
- Natural North American English TTS
- 100 varied starting questions
- Avoids the 10 most recently used starting questions during a session
- Local learning memory for recurring mistakes
- Structured JSON output for more reliable model responses

## Requirements

- Python 3.10+ (tested with a modern Python environment)
- An OpenAI API key with API billing enabled
- A microphone for voice practice

## Quick start — Windows

1. Clone or download this repository.
2. Run `setup_windows.bat` once.
3. Set your API key as a Windows user environment variable named `OPENAI_API_KEY`.
4. Close and reopen your terminal after setting the variable.
5. Double-click `start_windows.bat`.

You can also start it manually:

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

## Set the API key on Windows

PowerShell example:

```powershell
[Environment]::SetEnvironmentVariable(
    "OPENAI_API_KEY",
    "YOUR_KEY_HERE",
    "User"
)
```

Do **not** put a real API key in `app.py`, `.env.example`, screenshots, commits, or GitHub issues.

## Manual installation

```bash
python -m venv .venv
```

Activate the environment, then:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Project structure

```text
english-ai-coach/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── memory.example.json
├── setup_windows.bat
├── start_windows.bat
└── .github/
    └── workflows/
        └── python-check.yml
```

`memory.json` is created locally by the app and is intentionally ignored by Git because it contains personal learning history.

## OpenAI models used

The current app uses separate API calls for transcription, coaching, and text-to-speech. Model names are configured directly in `app.py` so they can be changed later if needed.

## Privacy and cost notes

Voice answers are sent to the OpenAI API for transcription, and conversation text is sent for coaching. Generated speech also uses the OpenAI API. API usage may incur charges according to your OpenAI API account and current pricing.

The local `memory.json` file stores a small list of recurring language mistakes. Delete it if you want to reset that local history.

## GitHub upload

Before pushing, verify that no secret is tracked:

```bash
git status
git diff --cached
```

Then create the repository history:

```bash
git init
git add .
git commit -m "Initial English AI Coach"
```

Create an empty repository on GitHub and follow GitHub's displayed commands to add the remote and push.

## License

No license is included yet. Add a license only after choosing the terms under which you want others to use or redistribute the project.


## macOS

### Requirements

- Python 3
- An OpenAI API key

### Quick setup

After cloning the repository:

```bash
cd english-ai-coach
chmod +x setup_macos.sh start_macos.sh
./setup_macos.sh
```

Set your OpenAI API key for the current Terminal session:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

Then start the app:

```bash
./start_macos.sh
```

To make the API key available in future Terminal sessions, add the export command to your shell profile (for example `~/.zshrc`) and reopen Terminal. Never commit your real API key to GitHub.

You can also start the app manually:

```bash
source .venv/bin/activate
python -m streamlit run app.py
```
