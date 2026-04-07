# Simple Research Agent

AI research agent powered by Google Gemini with Google Search grounding. Automatically searches, cross-verifies, and summarizes information from multiple sources in iterative steps.

## Project Structure

```
Simple_agent/
├── src/
│   ├── __init__.py
│   ├── config.py      # client, tools, and model configuration
│   ├── agent.py       # agent logic (run_agent)
│   └── main.py        # entry point
├── .env               # API key (do not commit!)
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Add your API key to the `.env` file:

```
GOOGLE_API_KEY=your_api_key
```

## Usage

```bash
python -m src.main
```

## How It Works

1. The agent receives a question from the user
2. Searches for information online (Google Search grounding)
3. Cross-verifies data against independent sources (up to 5 iterations)
4. Returns a verified summary with cited sources
