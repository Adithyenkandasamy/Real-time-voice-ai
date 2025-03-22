import os
import time
import dotenv
import sounddevice as sd
import numpy as np
import wave
from fasterwhisper_live import transcribe_audio  # Real-time transcription
from kokoro_tts_client import generate_kokoro_tts  # Text-to-Speech conversion
from github_openai import chat  # AI response from GPT-4o

dotenv.load_dotenv()

class AI_Assistant:
    def __init__(self):
        """Initialize AI Assistant with error handling and structured modules."""
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
        """Save the recorded audio to a file."""
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

    def transcribe_audio(self, audio_file_path):
        """Transcribe audio to text using Faster Whisper."""
        try:
            result = transcribe_audio(audio_file_path)
            if result:
                return result
            else:
                print("⚠️ Transcription failed. Please try speaking again.")
                return None
        except Exception as e:
            print(f"❌ Error in transcription: {e}")
            return None

    def generate_ai_response(self, transcript):
        """Generate AI response using GPT-4o."""
        try:
            print(f"\n👤 You: {transcript}")
            ai_response = chat(transcript)
            return ai_response
        except Exception as e:
            print(f"❌ Error in AI response generation: {e}")
            return "Sorry, something went wrong."

    def fast_stream_audio(self, text):
        """Generate and play voice response with Kokoro TTS."""
        try:
            audio_file = generate_kokoro_tts(text, voice="am_adam")
            if audio_file:
                time.sleep(0.5)  # Slight delay for a more natural response
                os.system(f"mpv {audio_file}")
            else:
                print("❌ Failed to generate voice response.")
        except Exception as e:
            print(f"❌ Error in TTS playback: {e}")

    def run_real_time_conversation(self):
        """Continuously listens, transcribes, and responds in real-time."""
        print("🎙️ Real-Time AI Assistant Started. Speak to begin!")

        while True:
            audio_data = self.record_audio(duration=5)  # Capture 5 seconds of audio
            
            if audio_data is None or audio_data.size == 0:  # Fix: Handle None & empty input
                print("⚠️ No audio detected. Please try speaking again.")
                continue

            audio_file = self.save_audio_file(audio_data)
            if not audio_file:
                print("❌ Failed to save audio file. Retrying...")
                continue

            transcript = self.transcribe_audio(audio_file)
            if not transcript or transcript.lower() == "transcription failed.":
                print("⚠️ Transcription failed. Please speak again.")
                continue  # Retry on failure

            ai_response = self.generate_ai_response(transcript)
            print(f"🤖 AI: {ai_response}")

            self.fast_stream_audio(ai_response)  # Convert AI response to speech

if __name__ == "__main__":
    assistant = AI_Assistant()
    assistant.run_real_time_conversation()
