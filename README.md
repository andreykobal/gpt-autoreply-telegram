
# Telegram AI AutoReply Bot

This repository contains the source code for a Telegram AI AutoReply bot. It utilizes Telethon to interact with Telegram API, OpenAI for generating text responses, and ElevenLabs for converting text responses into speech.

## Prerequisites

Before you can run the bot, you need to obtain API keys and install necessary dependencies. Here's how to get started:

### Obtain API Keys

1. **Telegram API ID and Hash**:
   - Go to [Telegram API](https://core.telegram.org/api/obtaining_api_id) and follow the instructions to receive your API ID and API Hash.

2. **OpenAI API Key**:
   - Obtain an API key from [OpenAI Platform](https://platform.openai.com/api-keys).

3. **ElevenLabs API Key**:
   - Sign up and get an API key from [ElevenLabs API](https://elevenlabs.io/docs/api-reference/react-text-to-speech-guide#get-an-api-key).

### Setup

Replace the placeholders in the code with your API keys and personal details where indicated:
- YOUR_API_ID
- YOUR_API_HASH
- YOUR_PHONE_NUMBER
- YOUR_PASSWORD
- YOUR_ELEVEN_LABS_API_KEY
- YOUR_OPENAI_API_KEY

### Environment Setup

- Create a Python virtual environment in your project directory:
  ```bash
  python -m venv venv
  ```

- Activate the virtual environment:
  ```bash
  source venv/bin/activate  # On Unix/macOS
  venv\Scripts\activate  # On Windows
  ```

- Install the required dependencies:
  ```bash
  pip install telethon openai elevenlabs json
  ```

## Running the Bot

- Start the bot by running:
  ```bash
  python main.py
  ```

- When the bot first runs, it will prompt you to enter the authentication code that you received in Telegram.

## Usage

Once the bot is running and authenticated, it will automatically reply to private messages using generated text and voice responses. You can enjoy interacting with your bot!

## Additional Information

- The `conversation_contexts/` directory will store the history of conversations to maintain context.
- Adjust the voice settings in `main.py` to customize the bot's speech output.

## Stopping the Bot

To stop the bot, simply interrupt the execution in your command line using `Ctrl+C`.

Enjoy your automated Telegram responses with AI-powered text and voice!
