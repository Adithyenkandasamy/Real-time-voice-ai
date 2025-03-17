import queue
import sounddevice as sd
import numpy as np
import faster_whisper

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    q.put(indata.copy())  # Store audio data as NumPy array

model = faster_whisper.WhisperModel("tiny", device="cpu")

with sd.InputStream(callback=callback, channels=1, samplerate=16000, dtype=np.float32, blocksize=4096):
    while True:
        audio = q.get()  # Get audio as NumPy array
        audio = np.squeeze(audio)  # Remove extra dimensions
        segments, _ = model.transcribe(audio, beam_size=5)
        
        for segment in segments:
            print(f"📝 Transcribed: {segment.text}")
