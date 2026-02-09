import os
from openai import OpenAI
from pathlib import Path
from datetime import datetime

def generate_audio(text, voice="alloy"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # 1. Define the path to the 'recordings' folder
    # This assumes 'recordings' is in the same folder as your notebook
    recordings_dir = Path("recordings")
    
    # 2. Create the folder if it doesn't exist
    recordings_dir.mkdir(parents=True, exist_ok=True)
    
    # 3. Create a unique filename using a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"podcast_{voice}_{timestamp}.mp3"
    speech_file_path = recordings_dir / filename

    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice.lower(),
            input=text
        )
        # 4. Save to the specific recordings path
        response.stream_to_file(speech_file_path)
        return str(speech_file_path)
    except Exception as e:
        print(f"TTS Error: {e}")
        return None