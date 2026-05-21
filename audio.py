import whisper
import sounddevice as sd
import numpy as np
import webrtcvad
import queue
import collections
import socket

# Settings
SAMPLERATE = 16000
FRAME_DURATION = 30  # ms
FRAME_SIZE = int(SAMPLERATE * FRAME_DURATION / 1000)
TRIGGER = "rocky"
HALLUCINATIONS = [
    "thank you", "thank you.", "thanks",
    "you", "bye", "goodbye", "the", "",
    "thank you so much", " "
]

model = whisper.load_model("small")
vad = webrtcvad.Vad(3)
audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    audio_queue.put(indata.copy())

def is_valid_speech(text):
    cleaned = text.lower().strip().rstrip('.')
    return cleaned not in HALLUCINATIONS

def transcribe(audio_data):
    audio = np.concatenate(audio_data)
    audio = np.squeeze(audio).astype(np.float32)
    result = model.transcribe(audio, language='en')
    return result["text"].strip()

def send(message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 9999))

    client.send(message.encode())
    

print("Rocky listening...")

with sd.InputStream(samplerate=SAMPLERATE, channels=1, callback=audio_callback, blocksize=FRAME_SIZE,device=0):
    triggered = False
    voiced_frames = []
    ring_buffer = collections.deque(maxlen=10)

    while True:
        chunk = audio_queue.get()
        chunk_int = (chunk * 32768).astype(np.int16)
        is_speech = vad.is_speech(chunk_int.tobytes(), SAMPLERATE)

        if not triggered:
            ring_buffer.append((chunk, is_speech))
            num_voiced = len([f for f, s in ring_buffer if s])
            if num_voiced > 7:
                triggered = True
                voiced_frames.extend([f for f, s in ring_buffer])
                ring_buffer.clear()
        else:
            voiced_frames.append(chunk)
            ring_buffer.append((chunk, is_speech))
            num_unvoiced = len([f for f, s in ring_buffer if not s])
            if num_unvoiced > 7:
                triggered = False
                text = transcribe(voiced_frames)
                voiced_frames = []
                ring_buffer.clear()

                if is_valid_speech(text):
                    print(f"Rocky heard: {text}")
                    #send(text)
                    if TRIGGER in text.lower():
                        print("Rocky triggered!") 
