# video_renderer.py
# Updated imports for MoviePy 2.1.1
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
import tempfile
import subprocess
import os

def make_video(img_dir, audio_paths, output_mp4, fps=1):
    clips = []
    imgs = sorted([f for f in os.listdir(img_dir) if f.endswith(".png")])
    
    for idx, img in enumerate(imgs):
        # Get the audio clip
        audio_clip = AudioFileClip(audio_paths[idx])
        
        # Create the image clip with the duration parameter
        img_clip = ImageClip(os.path.join(img_dir, img), duration=audio_clip.duration)
        
        # Directly assign the audio attribute instead of using set_audio method
        img_clip.audio = audio_clip
        
        clips.append(img_clip)
    
    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(output_mp4, fps=fps)
