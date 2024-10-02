import logging
import os
from TTS.api import TTS
import torch

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize TTS model
logger.info("Loading TTS model...")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tts = tts.to(device)
logger.info("TTS model loaded successfully")


def text_to_speech(text: str, output_file: str) -> None:
    """
    Convert text to speech and save it as an audio file.

    Args:
        text (str): The text to convert to speech.
        output_file (str): The path to save the generated audio file.

    Raises:
        Exception: For any errors during text-to-speech conversion.
    """
    try:
        logger.info(f"Converting text to speech: '{text}'")
        tts.tts_to_file(text=text,
                        file_path=output_file,
                        speaker="Ana Florence",
                        language="en",
                        split_sentences=True)
        logger.info(f"Speech saved to {output_file}")
    except Exception as e:
        logger.error(f"Error in text-to-speech conversion: {str(e)}")
        raise


def test_text_to_speech():
    """
    Test function for text_to_speech.
    """
    test_text = "This is a test for text-to-speech conversion."
    test_output = "test_tts_output.wav"
    try:
        text_to_speech(test_text, test_output)
        assert os.path.exists(test_output), f"Output file {test_output} not created"
        logger.info("text_to_speech test passed successfully")
    except Exception as e:
        logger.error(f"text_to_speech test failed: {str(e)}")
    # finally:
    #     if os.path.exists(test_output):
    #         os.remove(test_output)


if __name__ == "__main__":
    test_text_to_speech()
