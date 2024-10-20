# utils/audio_utils.py
import tempfile
import edge_tts


VOICES = [
    'en-US-AriaNeural', 'en-US-GuyNeural', 'en-GB-SoniaNeural', 'en-AU-NatashaNeural',
    'en-IN-NeerjaNeural', 'en-CA-ClaraNeural', 'en-NZ-MollyNeural', 'en-ZA-LeahNeural'
]

async def text_to_speech(text, voice='en-US-AriaNeural', rate='+0%', pitch='+0Hz'):
    communicate = edge_tts.Communicate(text, voice)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as audio_file:
        await communicate.save(audio_file.name)
        return audio_file.name