import os
import time
import dotenv
import speech_recognition as sr
from openai import OpenAI
import pyttsx3  # Import pyttsx3 for offline text-to-speech

# Load environment variables
dotenv.load_dotenv()

class AI_Assistant:
    def __init__(self):
        # Load API keys
        self.github_api_key = os.getenv("GITHUB_TOKEN")  # Use GitHub API token
        self.endpoint = "https://models.inference.ai.azure.com"

        # Validate API keys
        if not self.github_api_key:
            raise ValueError("Missing API key. Check your .env file.")

        # OpenAI GPT Model Setup (GitHub's GPT-4o)
        self.openai_client = OpenAI(
            api_key=self.github_api_key,
            base_url=self.endpoint
        )

        # System prompt for AI receptionist
        self.full_transcript = [
            {"role": "system", "content": "You are a receptionist at a dental clinic. Be resourceful and efficient."},
        ]

        # Initialize pyttsx3
        self.tts_engine = pyttsx3.init()
        voices = self.tts_engine.getProperty('voices')
        self.tts_engine.setProperty('rate', 120)
        self.tts_engine.setProperty('voice', voices[1].id)

    ###### Step 1: Capture Voice Input with SpeechRecognition ######

    def get_command(self):
        """ Capture a voice command using SpeechRecognition """
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

            try:
                print("Recognizing...")
                text = r.recognize_google(audio, language='en-in').lower()
                print(f"Detected: {text}")
                return text
            except Exception as e:
                print("Error recognizing speech:", e)
                return "None"

    ###### Step 2: Generate AI Response using GPT-4o ######

    def generate_ai_response(self, user_input):
        """ Process user input and generate AI response """
        if user_input in ["stop", "exit", "shutdown"]:
            print("Shutting down AI Assistant.")
            return

        self.full_transcript.append({"role": "user", "content": user_input})
        print(f"User: {user_input}")

        response = self.openai_client.chat.completions.create(
            model="gpt-4o",  # Use GPT-4o from GitHub's API
            messages=self.full_transcript
        )

        # Extract AI response
        ai_response = response.choices[0].message.content
        print(f"AI: {ai_response}")

        # Convert AI response to speech
        self.say(ai_response)

    ###### Step 3: Convert Text to Speech using pyttsx3 ######

    def say(self, text):
        """ Uses pyttsx3 to convert text to speech """
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

# Start AI Assistant
greeting = "Welcome to the AI Receptionist. How may I assist you today?"
ai_assistant = AI_Assistant()
ai_assistant.say(greeting)

while True:
    user_command = ai_assistant.get_command()
    if user_command in ["stop", "exit", "shutdown"]:
        ai_assistant.say("Goodbye!")
        break
    ai_assistant.generate_ai_response(user_command)
