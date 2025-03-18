import speech_recognition as sr

def get_command():
    """ Capture a voice command using SpeechRecognition """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("🎤 Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            print("🔍 Recognizing...")
            text = r.recognize_google(audio, language='en-in').lower()
            print(f"✅ Detected: {text}")
            return text
        except Exception as e:
            print("⚠️ Error recognizing speech:", e)
            return "None"
