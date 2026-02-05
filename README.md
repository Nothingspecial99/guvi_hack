# Agentic Honeypot System

An AI-powered honeypot to detect scams and autonomously engage scammers to extract intelligence.

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Copy `.env.example` to `.env` and set your keys:
   ```bash
   cp .env.example .env
   ```
   *Requires `GROQ_API_KEY`.*

3. **Run Server**
   ```bash
   python3 app/main.py
   ```
   Or directly with Uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```

## Architecture

- **FastAPI**: Public REST API.
- **ScamDetector**: Uses Heuristics + Groq LLM to classify intent.
- **PersonaAgent**: "Ramesh", a confused shopkeeper from Mumbai (using Groq Llama 3).
- **IntelligenceExtractor**: Regex-based extraction of UPI, Phones, URLs.
- **SessionManager**: Tracks state (Scam Confirmed, Message Count).
- **CallbackService**: Reports final analysis to evaluation endpoint.

## API Usage

**Endpoint:** `POST /api/v1/chat`
**Headers:** `x-api-key: YOUR_SECRET_KEY`

**Payload:**
```json
{
  "sessionId": "test-123",
  "message": {
    "sender": "scammer",
    "text": "You won 1 Crore! Send 5000 rs processing fee to claiming.",
    "timestamp": 1700000000
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "WhatsApp",
    "language": "en",
    "locale": "IN"
  }
}
```

## Features

- **Stealth**: Agent acts like a naive user, never reveals it's a bot.
- **Extraction**: Silently records UPI IDs and Phone numbers.
- **Safety**: Does not threaten laws, just wastes scammer time.
- **Reporting**: Auto-posts to hackathon callback after engagement.
