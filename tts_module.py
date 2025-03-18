import time
from elevenlabs import generate, play

def fast_stream_audio(text, voice):
    """ Streams AI-generated voice with lower latency """
    start_time = time.time()

    try:
        # Stream directly from ElevenLabs
        audio = generate(text=text, voice=voice, model="eleven_multilingual_v2")
        play(audio)

    except Exception as e:
        print(f"❌ Error in audio streaming: {e}")

    end_time = time.time()
    print(f"⏳ Response Time: {end_time - start_time:.2f} seconds")
