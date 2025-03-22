import os
import time
import dotenv
from elevenlabs import set_api_key, generate
from openai import OpenAI
from fasterwhisper_live import transcribe_audio  # Import from local file

# Load environment variables
dotenv.load_dotenv()

class AI_Assistant:
    def __init__(self):
        # Load API keys
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        # Validate API keys
        if not all([self.elevenlabs_api_key, self.openai_api_key]):
            raise ValueError("⚠️ Missing one or more API keys. Check your .env file.")

        # Set ElevenLabs API Key
        set_api_key(self.elevenlabs_api_key)

        # OpenAI GPT Model Setup
        self.openai_client = OpenAI(api_key=self.openai_api_key)

        # System prompt for AI receptionist
        self.full_transcript = [
            {"role": "system", "content": "You are a receptionist at a dental clinic. Be resourceful and efficient."},
        ]

        # Set default ElevenLabs voice
        self.voice = "Daniel"

    def transcribe_audio(self, audio_file_path):
        """Transcribe audio using Faster Whisper"""
        try:
            result = transcribe_audio(audio_file_path)  # Call the local function
            return result if result else "Transcription failed."
        except Exception as e:
            print(f"❌ Error in transcription: {e}")
            return None

    def generate_ai_response(self, transcript):
        """Process user input and generate AI response"""
        self.full_transcript.append({"role": "user", "content": transcript})
        print(f"\n👤 Patient: {transcript}", end="\r\n")

        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=self.full_transcript
        )

        ai_response = response.choices[0].message.content
        return ai_response

    def fast_stream_audio(self, text):
        """Streams AI-generated voice with lower latency"""
        start_time = time.time()

        try:
            audio = generate(text=text, voice="Daniel", model="eleven_multilingual_v2")
            return audio
        except Exception as e:
            print(f"❌ Error in audio streaming: {e}")
            return None
