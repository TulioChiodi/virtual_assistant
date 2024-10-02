import whisper

# Initialize Whisper model (consider loading once)
whisper_model = whisper.load_model('large')


def transcribe_audio(filename='input_audio.wav'):
    result = whisper_model.transcribe(filename)
    return result['text']
