import os
import whisper
import logging
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Whisper model (consider loading once)
whisper_model = whisper.load_model(os.getenv('WHISPER_MODEL'))


def transcribe_audio(filename=os.getenv('INPUT_AUDIO_FILE')):
    """
    Transcribe the given audio file using the Whisper model.

    Args:
        filename (str): Path to the audio file to transcribe. Defaults to the value of INPUT_AUDIO_FILE in .env.

    Returns:
        str: The transcribed text from the audio file.

    Raises:
        FileNotFoundError: If the audio file is not found.
        Exception: For any other errors during transcription.
    """
    try:
        logger.info(f"Starting transcription of file: {filename}")
        result = whisper_model.transcribe(filename, language="en")
        transcribed_text = result['text']
        logger.info("Transcription completed successfully")
        return transcribed_text
    except FileNotFoundError:
        logger.error(f"Audio file not found: {filename}")
        raise
    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
        raise


# Test function for transcribe_audio
def test_transcribe_audio():
    # Create a short test audio file
    test_filename = "test_audio.wav"
    os.system(f"echo 'This is a test audio file' | text2wave -o {test_filename}")

    try:
        transcribed_text = transcribe_audio(test_filename)
        assert "test audio file" in transcribed_text.lower(), "Transcription doesn't match expected content"
        print("Transcription test passed successfully")
    except Exception as e:
        print(f"Transcription test failed: {str(e)}")
    finally:
        # Clean up the test file
        os.remove(test_filename)


if __name__ == "__main__":
    test_transcribe_audio()
