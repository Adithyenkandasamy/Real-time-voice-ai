from vosk import Model, KaldiRecognizer
import pyaudio

model = Model("vosk-model-en-us-0.22")
recognizer = KaldiRecognizer(model, 16000)

def real_time_transcribe():
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = result.split('"')[3]  # Extract transcript
            return text
