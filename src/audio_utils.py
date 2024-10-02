# audio_utils.py

import os
import pyaudio
import wave
import subprocess
import logging
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Audio recording parameters
FORMAT = getattr(pyaudio, os.getenv('AUDIO_FORMAT'))
CHANNELS = int(os.getenv('AUDIO_CHANNELS'))
RATE = int(os.getenv('AUDIO_RATE'))
CHUNK = int(os.getenv('AUDIO_CHUNK'))
RECORD_SECONDS = int(os.getenv('RECORD_SECONDS'))


def record_audio(filename=os.getenv('INPUT_AUDIO_FILE')):
    """
    Record audio from the microphone and save it to a file.

    Args:
        filename (str): Path to save the recorded audio file. Defaults to the value of INPUT_AUDIO_FILE in .env.

    Raises:
        Exception: For any errors during audio recording or saving.
    """
    try:
        logger.info(f"Starting audio recording to file: {filename}")
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        logger.info("Listening...")
        frames = []
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        logger.info("Finished recording.")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        save_audio(frames, filename)
        logger.info(f"Audio saved to {filename}")
    except Exception as e:
        logger.error(f"Error during audio recording: {str(e)}")
        raise


def save_audio(frames, filename):
    """
    Save recorded audio frames to a WAV file.

    Args:
        frames (list): List of audio frames.
        filename (str): Path to save the audio file.

    Raises:
        Exception: For any errors during file saving.
    """
    try:
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
    except Exception as e:
        logger.error(f"Error saving audio file: {str(e)}")
        raise


def play_audio(filename):
    """
    Play an audio file using the system's default audio player.

    Args:
        filename (str): Path to the audio file to play.

    Raises:
        FileNotFoundError: If the audio file is not found.
        Exception: For any other errors during playback.
    """
    try:
        logger.info(f"Playing audio file: {filename}")
        subprocess.run(["aplay", filename], check=True)
        logger.info("Audio playback completed")
    except FileNotFoundError:
        logger.error(f"Audio file not found: {filename}")
        raise
    except Exception as e:
        logger.error(f"Error during audio playback: {str(e)}")
        raise


def test_audio_utils():
    """
    Test function for audio utilities.
    """
    test_filename = "test_audio.wav"
    try:
        logger.info("Testing audio utilities...")
        record_audio(test_filename)
        assert os.path.exists(test_filename), "Recorded audio file not found"
        play_audio(test_filename)
        logger.info("Audio utility tests completed successfully")
    except Exception as e:
        logger.error(f"Audio utility test failed: {str(e)}")
    finally:
        if os.path.exists(test_filename):
            os.remove(test_filename)


if __name__ == "__main__":
    test_audio_utils()
