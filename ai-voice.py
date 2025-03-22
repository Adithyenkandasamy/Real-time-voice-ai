import os
import time
import dotenv
import sounddevice as sd
import numpy as np
import wave
from fasterwhisper_live import transcribe_audio  # Real-time transcription
from kokoro_tts_client import generate_kokoro_tts  # Text-to-Speech conversion
from github_openai import chat  # AI response from GPT-4o

# Load environment variables
dotenv.load_dotenv()

class AI_Assistant:
    def __init__(self):
        """Initialize AI Assistant for real-time transcription and AI responses."""
        self.full_transcript = [
            {"role": "system", "content": "You're a friendly and casual AI assistant. "
                                          "Talk like a best friend, keeping the conversation natural and fun. "
                                          "Avoid unnecessary symbols like @#$%^&*. "
                                          "Make responses smooth and engaging, just like a normal human chat."},
        ]

    def record_audio(self, duration=5, samplerate=16000):
        """Record audio from the microphone in real-time."""
        print("🎤 Listening... Speak now!")
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
        sd.wait()  # Wait for the recording to finish
        return np.squeeze(audio_data)  # Return raw audio data

    def save_audio_file(self, audio_data, filename="input.wav", samplerate=16000):
        """Save recorded audio to a file."""
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            wf.writeframes(audio_data.tobytes())
        return filename

    def transcribe_audio(self, audio_file_path):
        """Transcribe audio using Faster Whisper."""
        try:
            result = transcribe_audio(audio_file_path)
            return result if result else "Transcription failed."
        except Exception as e:
            print(f"❌ Error in transcription: {e}")
            return None

    def generate_ai_response(self, transcript):
        """Generate a real-time AI response using GPT-4o."""
        print(f"\n👤 You: {transcript}")

        ai_response = chat(transcript)  # Call GPT-4o chat function
        return ai_response

    def fast_stream_audio(self, text):
        """Generate and play voice response using Kokoro TTS."""
        audio_file = generate_kokoro_tts(text, voice="af_nova")

        if audio_file:
            os.system(f"mpv {audio_file}")  # Play the generated audio
        else:
            print("❌ Failed to generate voice response.")

    def run_real_time_conversation(self):
        """Continuously listens, transcribes, and responds in real-time."""
        print("🎙️ Real-Time AI Assistant Started. Speak to begin!")

        while True:
            audio_data = self.record_audio(duration=5)  # Capture 5 seconds of audio
            audio_file = self.save_audio_file(audio_data)

            transcript = self.transcribe_audio(audio_file)
            if not transcript:
                print("⚠️ No speech detected. Try speaking again.")
                continue

            ai_response = self.generate_ai_response(transcript)
            print(f"🤖 AI: {ai_response}")

            self.fast_stream_audio(ai_response)  # Convert AI response to speech


# Run the assistant
if __name__ == "__main__":
    assistant = AI_Assistant()
    assistant.run_real_time_conversation()
