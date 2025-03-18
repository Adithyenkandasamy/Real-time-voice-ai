import os
import dotenv
from elevenlabs import set_api_key
from speech_recognition_module import get_command
from tts_module import fast_stream_audio
from gpt_module import GPTModel

# Load environment variables
dotenv.load_dotenv()

class AI_Assistant:
    def __init__(self):
        # Load API keys
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.github_api_key = os.getenv("GITHUB_TOKEN")  # Use GitHub API token
        self.endpoint = "https://models.inference.ai.azure.com"

        # Validate API keys
        if not all([self.elevenlabs_api_key, self.github_api_key]):
            raise ValueError("⚠️ Missing one or more API keys. Check your .env file.")

        # Set ElevenLabs API Key
        set_api_key(self.elevenlabs_api_key)

        # Initialize GPT Model
        self.gpt_model = GPTModel(api_key=self.github_api_key, endpoint=self.endpoint)

        # Set default ElevenLabs voice
        self.voice = "Daniel"  # Change to any supported voice

    def get_command(self):
        return get_command()

    def generate_ai_response(self, user_input):
        ai_response = self.gpt_model.generate_ai_response(user_input)
        if ai_response:
            fast_stream_audio(ai_response, self.voice)

    def fast_stream_audio(self, text):
        fast_stream_audio(text, self.voice)

# Start AI Assistant
greeting = "Welcome to the AI Receptionist. How may I assist you today?"
ai_assistant = AI_Assistant()
ai_assistant.fast_stream_audio(greeting)

while True:
    user_command = ai_assistant.get_command()
    if user_command in ["stop", "exit", "shutdown"]:
        ai_assistant.fast_stream_audio("Goodbye!")
        break
    ai_assistant.generate_ai_response(user_command)
