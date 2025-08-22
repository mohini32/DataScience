# CLI Chatbot

A simple command-line chatbot with support for multiple AI APIs including free options.

## Features

- **Multiple AI Providers**: Support for Google Gemini API and local Hugging Face models
- **Free Options**: Completely free offline mode with local models
- **Streaming**: Real-time response streaming for better user experience
- **Conversation History**: Maintains context across the conversation
- **Rate Limiting**: Built-in rate limiting and error handling
- **Easy Configuration**: Simple config file setup

## Supported APIs

1. **Simple Rule-Based** (Default - Completely free)
   - No API keys required
   - Works offline
   - Instant responses
   - Great for basic conversations

2. **Google Gemini API** (Free tier available)
   - Generous free quota
   - Fast responses
   - High quality AI responses

3. **Hugging Face Transformers** (Completely free)
   - Runs locally
   - No API keys needed
   - Works offline
   - Requires additional setup

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your API keys (optional for local mode):
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Usage

### Quick Start (No setup required)
```bash
python chatbot.py
```
This will start with the simple rule-based chatbot that works immediately!

### Using Google Gemini API
1. Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add it to your `.env` file:
   ```
   GOOGLE_API_KEY=your_api_key_here
   AI_PROVIDER=gemini
   ```
3. Run: `python chatbot.py --provider gemini`

### Using Hugging Face (Advanced)
1. Install additional dependencies:
   ```bash
   pip install transformers torch
   ```
2. Run: `python chatbot.py --provider huggingface`

## Commands

- `exit` or `quit`: Exit the chatbot
- `clear`: Clear conversation history
- `history`: Show conversation history
- `save`: Save conversation to file
- `config`: Show current configuration
- `help`: Show available commands

## Configuration

Edit the `.env` file to configure your preferred AI provider and API keys.
