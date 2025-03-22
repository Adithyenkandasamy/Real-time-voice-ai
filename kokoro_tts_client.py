import requests

# Kokoro TTS API Endpoint
API_URL = "http://127.0.0.1:8880/v1/audio/speech"  # Change port if needed

# Function to call Kokoro TTS and save the output as an MP3 file
def generate_tts(text, model="kokoro", voice="af_nova", response_format="mp3"):
    payload = {
        "model": model,
        "input": text,
        "voice": voice,
        "response_format": response_format
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        # Save the audio file
        audio_file = "output.mp3"
        with open(audio_file, "wb") as f:
            f.write(response.content)
        print(f"✅ Audio saved as {audio_file}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

# Example Usage
if __name__ == "__main__":
    text_to_speak = "naruto uzumaki from leaf village"
    generate_tts(text_to_speak)
