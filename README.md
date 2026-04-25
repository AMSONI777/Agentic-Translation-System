# Agentic Translation System

A modular, AI-powered translation platform built with SOLID design principles, dual-backend support, and an agentic workflow architecture.

## Features

- **Text Translation** — Translate text between 16+ languages with auto-detection
- **Audio Translation** — Upload an audio file and get transcription + translation
- **Conversation Memory** — Full history stored per session with session isolation
- **Real-Time Audio** — Record your voice and get streaming translation instantly

## Tech Stack

- Python 3.10+
- Streamlit (UI)
- Groq API — LLaMA 3.3 70B (translation) + Whisper Large v3 (transcription)
- CmsAI API — Professor-provided on-campus backend (optional)

## Architecture

The system follows SOLID design principles with an agentic workflow:

- `LLMProvider` interface — implemented by `CmsAIProvider` and `GroqProvider`
- `TranscriptionProvider` interface — implemented by `GroqWhisperProvider`
- `MemoryStore` interface — implemented by `InMemoryStore`
- `LanguageDetectionAgent` — builds translation prompts
- `TranslationAgent` — handles LLM calls
- `TranscriptionAgent` — handles audio transcription
- `StreamingTranslationAgent` — handles real-time streaming
- `Orchestrator` — coordinates all agents and memory
- `app.py` — Streamlit UI, only talks to Orchestrator

## Setup

```bash
git clone git@github.com:AMSONI777/Agentic-Translation-System.git
cd Agentic-Translation-System
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Backend Switching

Change `PROVIDER` in `.env` to switch backends:
