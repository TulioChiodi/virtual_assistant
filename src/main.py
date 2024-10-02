# main.py

import os
import logging
from dotenv import load_dotenv
from audio_utils import record_audio, play_audio
from transcription import transcribe_audio
from llm_interface import generate_response
from tts_utils import text_to_speech
from conversation_manager import ConversationManager

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """
    Main function to run the conversational AI system.
    This function orchestrates the conversation loop, including audio recording,
    transcription, response generation, and text-to-speech conversion.
    """
    # Initialize Conversation Manager with system message
    system_message = os.getenv('SYSTEM_MESSAGE')
    conversation = ConversationManager(system_message)
    logger.info("Conversation started")

    while True:
        try:
            # Record audio
            logger.info("Recording audio...")
            record_audio(os.getenv('INPUT_AUDIO_FILE'))

            # Transcribe audio
            logger.info("Transcribing audio...")
            input_text = transcribe_audio(os.getenv('INPUT_AUDIO_FILE'))
            logger.info(f"Transcribed Text: {input_text}")

            # Generate response
            logger.info("Generating AI response...")
            conversation_history = conversation.get_history()
            response = generate_response(conversation_history, input_text)
            logger.info(f"AI Response: {response}")

            # Update conversation history
            conversation.update_history(input_text, response)

            # Convert response to speech
            logger.info("Converting response to speech...")
            text_to_speech(response, os.getenv('OUTPUT_AUDIO_FILE'))

            # Play generated audio
            logger.info("Playing AI response...")
            play_audio(os.getenv('OUTPUT_AUDIO_FILE'))

            # Ask if the user wants to continue
            user_choice = input("Do you want to continue the conversation? (yes/no): ").lower()
            if user_choice != 'yes':
                break

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            break

    logger.info("Conversation ended.")


if __name__ == "__main__":
    main()
