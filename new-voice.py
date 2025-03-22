import os
import time
import json
import dotenv
import wave
import subprocess
import numpy as np
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import openai
from kokoro_tts_client import generate_kokoro_tts  # Text-to-Speech conversion

dotenv.load_dotenv()

# Vosk Model Path (Ensure it exists)
VOSK_MODEL_PATH = "/home/jinwoo/Desktop/Real-time-voice-ai/vosk-model-small-en-us-0.15"

# Load Vosk Model
if not os.path.exists(VOSK_MODEL_PATH):
    print(f"❌ Model folder '{VOSK_MODEL_PATH}' not found. Check the path.")
    exit(1)

vosk_model = Model(VOSK_MODEL_PATH)

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("GITHUB_TOKEN")  # Set this in .env
OPENAI_ENDPOINT = "https://models.inference.ai.azure.com"
MODEL_NAME = "gpt-4o"  # Change to "DeepSeek-R1" if needed

client = openai.AzureOpenAI(
    api_key=OPENAI_API_KEY,
    api_version="2023-05-15",
    azure_endpoint=OPENAI_ENDPOINT
)

def chat(user_message):
    """Get AI response from OpenAI/Azure in real-time."""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You're a friendly AI assistant, speaking casually."},
            {"role": "user", "content": user_message},
        ],
        stream=True  # Enable streaming
    )

    full_response = ""
    for chunk in response:
        if chunk.choices and chunk.choices[0].delta:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_response += content  # Store the full response

    print("\n")  # Add spacing after response
    return full_response

class AI_Assistant:
    def __init__(self):
        """Initialize AI Assistant with Vosk for STT and OpenAI for AI responses."""
        self.recognizer = KaldiRecognizer(vosk_model, 16000)
        self.full_transcript = []

    def record_audio(self, duration=5, samplerate=16000):
        """Record audio from the microphone."""
        try:
            print("🎤 Listening... Speak now!")
            audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
            sd.wait()
            return np.squeeze(audio_data)
        except Exception as e:
            print(f"❌ Error recording audio: {e}")
            return None

    def save_audio_file(self, audio_data, filename="input.wav", samplerate=16000):
        """Save the recorded audio as WAV."""
        try:
            with wave.open(filename, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(samplerate)
                wf.writeframes(audio_data.tobytes())
            return filename
        except Exception as e:
            print(f"❌ Error saving audio file: {e}")
            return None

    def convert_mp3_to_wav(self, mp3_path, wav_path="temp.wav"):
        """Convert MP3 to WAV using FFmpeg."""
        command = ["ffmpeg", "-i", mp3_path, "-ac", "1", "-ar", "16000", "-sample_fmt", "s16", wav_path, "-y"]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return wav_path

    def transcribe_audio(self, audio_file_path):
        """Transcribe audio to text using Vosk."""
        try:
            with wave.open(audio_file_path, "rb") as wf:
                if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
                    print("⚠️ Audio must be mono, 16-bit, and 16kHz. Convert it before processing.")
                    return None
                
                recognizer = KaldiRecognizer(vosk_model, wf.getframerate())
                transcript = ""

                while True:
                    data = wf.readframes(4000)
                    if not data:
                        break
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        transcript += result.get("text", "") + " "

                return transcript.strip()
        except Exception as e:
            print(f"❌ Error in transcription: {e}")
            return None

    def generate_ai_response(self, transcript):
        """Generate AI response using OpenAI/Azure."""
        try:
            print(f"\n👤 You: {transcript}")
            ai_response = chat(transcript)  # Calls OpenAI API
            return ai_response
        except Exception as e:
            print(f"❌ Error in AI response: {e}")
            return "Sorry, something went wrong."

    def fast_stream_audio(self, text):
        """Generate and play voice response with Kokoro TTS."""
        try:
            audio_file = generate_kokoro_tts(text, voice="am_adam")
            if audio_file:
                time.sleep(0.5)  # Natural response delay
                os.system(f"mpv {audio_file}")  # Play TTS response
            else:
                print("❌ Failed to generate voice response.")
        except Exception as e:
            print(f"❌ Error in TTS playback: {e}")

    def run_real_time_conversation(self):
        """Continuously listens, transcribes, and responds in real-time."""
        print("🎙️ Real-Time AI Assistant Started. Speak to begin!")

        while True:
            audio_data = self.record_audio(duration=5)  # Capture 5 seconds of audio
            
            if audio_data is None or audio_data.size == 0:
                print("⚠️ No audio detected. Please try speaking again.")
                continue

            audio_file = self.save_audio_file(audio_data)
            if not audio_file:
                print("❌ Failed to save audio file. Retrying...")
                continue

            transcript = self.transcribe_audio(audio_file)
            if not transcript or transcript.lower() == "transcription failed.":
                print("⚠️ Transcription failed. Please speak again.")
                continue  

            ai_response = self.generate_ai_response(transcript)
            print(f"🤖 AI: {ai_response}")

            self.fast_stream_audio(ai_response)  # Convert AI response to speech

if __name__ == "__main__":
    assistant = AI_Assistant()
    assistant.run_real_time_conversation()
