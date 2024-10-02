# audio_utils.py

import pyaudio
import wave
import subprocess

# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5


def record_audio(filename='input_audio.wav'):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Listening...")
    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    save_audio(frames, filename)


def save_audio(frames, filename):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def play_audio(filename):
    subprocess.run(["aplay", filename])


if __name__ == "__main__":
    print("Testing audio utilities...")

    # Test recording
    test_filename = "test_audio.wav"
    print(f"Recording audio to {test_filename}...")
    record_audio(test_filename)

    # Test playing
    print(f"Playing recorded audio from {test_filename}...")
    play_audio(test_filename)

    print("Audio utility tests completed.")
