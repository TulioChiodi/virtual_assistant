# Conversational AI Project

This project is a conversational AI system that uses:

- **Whisper** for speech-to-text transcription.
- **Ollama LLM** for generating AI responses.
- **Coqui TTS** for text-to-speech conversion.

## Project Structure

- `main.py`: Main script to run the conversation.
- `audio_utils.py`: Handles audio recording and playback.
- `transcription.py`: Transcribes audio using Whisper.
- `llm_interface.py`: Interfaces with the LLM via Ollama SDK.
- `tts_utils.py`: Converts text to speech using Coqui TTS.
- `conversation_manager.py`: Manages the conversation history.

## Requirements

- Python 3.x
- See `requirements.txt` for Python package dependencies.

## Setup Instructions

1. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:


   ```bash
   source venv/bin/activate
   ```

3. Install Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the main script:

   ```bash
   python main.py
   ```