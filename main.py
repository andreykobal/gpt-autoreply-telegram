import time
from telethon import TelegramClient, events
import openai
import character_info
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings
import json
import os

# Telegram and ElevenLabs API credentials, and other details
api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'
phone = 'YOUR_PHONE_NUMBER'
session_file = 'session'
password = 'YOUR_PASSWORD'
elevenlabs_api_key = "YOUR_ELEVEN_LABS_API_KEY"

# OpenAI API setup
openai_client = openai.OpenAI(api_key="YOUR_OPENAI_API_KEY")

characterName = "Carolina"
characterBio = "Calming minds and soothing souls, you guide people toward tranquility through meditation."

# Create the ElevenLabs and Telegram clients
eleven_client = ElevenLabs(api_key=elevenlabs_api_key)
client = TelegramClient(session_file, api_id, api_hash, sequential_updates=True)

# Constants for managing conversation history
max_context_length = 2048
base_context_path = 'conversation_contexts/'

# Set up custom voice settings
voice_settings = VoiceSettings(
    stability=0.5,  # Adjust stability, range 0-1 where 1 is most stable
    similarity_boost=1,  # Boosts similarity to the chosen voice model
    style=1,  # Adjusts the speaking style
    use_speaker_boost=True  # Enhances the speaker's voice characteristics
)

custom_voice = Voice(
    voice_id='Atp5cNFg1Wj5gyKD7HWV',  # Example voice ID, replace with your actual voice ID
    settings=voice_settings
)

def get_context_file_path(username):
    """Generate file path for user-specific conversation context."""
    directory = os.path.join(base_context_path, username)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return os.path.join(directory, 'context.json')

def load_conversation_context(file_path):
    """Load conversation context from a user-specific JSON file."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get('context', '')
    except (FileNotFoundError, json.JSONDecodeError):
        return ""

def save_conversation_context(context, file_path):
    """Save conversation context to a user-specific JSON file."""
    with open(file_path, 'w') as file:
        json.dump({'context': context}, file)

def trim_conversation_context(context):
    """Ensures the conversation context does not exceed the maximum allowed length."""
    while len(context) > max_context_length:
        first_newline_index = context.find('\n')
        if first_newline_index != -1:
            context = context[first_newline_index + 1:]
        else:
            context = ""  # Clear context if no newline is found
    return context

@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    if event.is_private:
        from_ = await event.get_sender()
        recipientName = from_.first_name  # Use a consistent identifier like username or user_id
        file_path = get_context_file_path(recipientName)

        if not from_.bot:
            conversation_context = load_conversation_context(file_path)
            conversation_context += f"{recipientName}: {event.text}\n"
            conversation_context = trim_conversation_context(conversation_context)
            save_conversation_context(conversation_context, file_path)

            systemPrompt = f"You are {characterName}. {characterBio}. Behave like a real person, keep the conversation going."
            prompt = f"Give a reply to {recipientName}; given the context of the conversation: {conversation_context}. {characterName}:"

            completion = openai_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": systemPrompt},
                    {"role": "user", "content": prompt},
                ],
                model="gpt-3.5-turbo",
            )

            response_text = completion.choices[0].message.content
            conversation_context += f"{characterName}: {response_text}\n"
            conversation_context = trim_conversation_context(conversation_context)
            save_conversation_context(conversation_context, file_path)

            audio_generator = eleven_client.generate(
                text=response_text, 
                voice=custom_voice
            )
            audio_path = f"{base_context_path}/{recipientName}/response.mp3"
            with open(audio_path, "wb") as f:
                for chunk in audio_generator:
                    f.write(chunk)

            time.sleep(1)
            await event.respond(file=audio_path)

            #comment the elevenlabs code and uncomment this if you want text responses
            #await event.respond(response_text)


if __name__ == '__main__':
    print(time.asctime(), '-', 'Auto-replying...')
    client.start(phone, password)
    client.run_until_disconnected()
    print(time.asctime(), '-', 'Stopped!')
