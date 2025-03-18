from elevenlabs import generate, play, set_api_key

# Set your API key
set_api_key("sk_3a076382aa26fdd30418b2a326af78878948ceb67e9fce25")

# Generate audio from text
audio = generate(
    text="Hello! This is a test of ElevenLabs voice generation.",
    voice="Daniel",  # Change to your preferred voice
    model="eleven_multilingual_v2"
)

# Play the generated audio
play(audio)
