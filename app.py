import os
import openai
import json
import pyttsx3
import numpy as np
import pyaudio
import time
import wave

from message import Message, Prompt, Response
from dotenv import load_dotenv

load_dotenv()
engine = pyttsx3.init()
engine.setProperty("rate", 150)
openai.api_key = os.getenv("OPENAI_API_KEY")


def is_silent(data, threshold):
    """Returns True if the audio data is silent, False otherwise."""
    return np.abs(data).mean() < threshold


def record_audio_until_silence(filename, threshold=300, silence_duration=2):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    silence_start_time = None

    while True:
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        frames.append(data)

        if is_silent(data, threshold):
            if silence_start_time is None:
                silence_start_time = time.time()
            elif time.time() - silence_start_time >= silence_duration:
                break
        else:
            silence_start_time = None

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio to a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))


def main():
    print("Recording...")
    record_audio_until_silence("user_voice.wav")
    print("Finished recording")

    audio_file= open("user_voice.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript["text"])

    resp = Response(
        openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[Prompt(transcript["text"]).to_dict()],
        )["choices"][0]["message"]["content"]
    )

    engine.say(resp.content)
    engine.runAndWait()
    engine.stop()


if __name__ == "__main__":
    main()
