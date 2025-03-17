import os
import time
import dotenv
import assemblyai as aai
from elevenlabs import set_api_key, generate, play
from openai import OpenAI

# Load environment variables
dotenv.load_dotenv()

class AI_Assistant:
    def __init__(self):
        # Load API keys
        self.aai_api_key = os.getenv("ASSEMBLYAI_API_KEY")
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        # Validate API keys
        if not all([self.aai_api_key, self.elevenlabs_api_key, self.openai_api_key]):
            raise ValueError("⚠️ Missing one or more API keys. Check your .env file.")

        # Set ElevenLabs API Key
        set_api_key(self.elevenlabs_api_key)

        # OpenAI GPT Model Setup
        self.openai_client = OpenAI(api_key=self.openai_api_key)

        self.transcriber = None

        # System prompt for AI receptionist
        self.full_transcript = [
            {"role": "system", "content": "You are a receptionist at a dental clinic. Be resourceful and efficient."},
        ]

        # Set default ElevenLabs voice
        self.voice = "Daniel"  # Change to any supported voice

    ###### Step 1: Real-Time Transcription with AssemblyAI ######

    def start_transcription(self):
        """ Start real-time speech transcription """
        self.transcriber = aai.RealtimeTranscriber(
            sample_rate=16000,
            on_data=self.on_data,
            on_error=self.on_error,
            on_open=self.on_open,
            on_close=self.on_close,
            end_utterance_silence_threshold=1000
        )

        self.transcriber.connect()
        microphone_stream = aai.extras.MicrophoneStream(sample_rate=16000)
        self.transcriber.stream(microphone_stream)

    def stop_transcription(self):
        """ Stop transcription """
        if self.transcriber:
            self.transcriber.close()
            self.transcriber = None

    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        return 

    def on_data(self, transcript: aai.RealtimeTranscript):
        """ Handle live transcription data """
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            self.generate_ai_response(transcript)
        else:
            print(transcript.text, end="\r")

    def on_error(self, error: aai.RealtimeError):
        print("❌ Error:", error)

    def on_close(self):
        pass

    ###### Step 2: Generate AI Response using GPT-4o ######

    def generate_ai_response(self, transcript):
        """ Process user input and generate AI response """
        self.stop_transcription()

        self.full_transcript.append({"role": "user", "content": transcript.text})
        print(f"\n👤 Patient: {transcript.text}", end="\r\n")

        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=self.full_transcript
        )

        ai_response = response.choices[0].message.content
        self.fast_stream_audio(ai_response)  # ✅ Faster streaming integration

        self.start_transcription()
        print(f"\n🎤 Listening again...", end="\r\n")

    ###### Step 3: Optimized Real-Time Audio Streaming ######

    def fast_stream_audio(self, text):
        """ Streams AI-generated voice with lower latency """
        start_time = time.time()

        try:
            # Stream directly from ElevenLabs
            audio = generate(text="Hello", voice="Daniel", model="eleven_multilingual_v2")
            play(audio)

        except Exception as e:
            print(f"❌ Error in audio streaming: {e}")

        end_time = time.time()
        print(f"⏳ Response Time: {end_time - start_time:.2f} seconds")

# Start AI receptionist
greeting = "Thank you for calling Vancouver dental clinic. My name is Sandy, how may I assist you?"
ai_assistant = AI_Assistant()
ai_assistant.fast_stream_audio(greeting)
ai_assistant.start_transcription()
