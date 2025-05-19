# tts_renderer.py
from gtts import gTTS
import json, os

def render_tts(script_json, audio_dir):
    os.makedirs(audio_dir, exist_ok=True)
    slides = json.loads(script_json)
    audio_paths = []
    for idx, s in enumerate(slides):
        t = gTTS(s["narration"], lang="en")
        path = os.path.join(audio_dir, f"slide_{idx}.mp3")
        t.save(path)
        audio_paths.append(path)
    return audio_paths
