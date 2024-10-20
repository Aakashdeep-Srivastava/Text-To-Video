# utils/video_utils.py
import os
from moviepy.editor import ImageClip, concatenate_videoclips, CompositeVideoClip, AudioFileClip, concatenate_audioclips, TextClip, ColorClip
# Ensure ImageMagick is properly configured
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})  # Replace with your actual path

def create_slide(title, points, image_path, audio_file):
    # Define slide dimensions (16:9 aspect ratio)
    slide_width, slide_height = 1280, 720
    
    # Get audio duration
    audio_clip = AudioFileClip(audio_file)
    audio_duration = audio_clip.duration
    
    # Create a white background
    background = ColorClip(size=(slide_width, slide_height), color=(255, 255, 255)).set_duration(audio_duration)
    
    # Load the resized image
    image = ImageClip(image_path).set_duration(audio_duration)
    
    # Create title text
    title_clip = TextClip(title, fontsize=40, color='black', size=(slide_width - 80, None), method='caption', font='Arial-Bold')
    title_clip = title_clip.set_position(('center', 50)).set_duration(audio_duration)
    
    # Create bullet points
    bullet_clips = []
    for i, point in enumerate(points):
        bullet = TextClip(f"• {point}", fontsize=30, color='black', size=(slide_width - 100, None), method='caption', font='Arial')
        bullet = bullet.set_position((50, 150 + i*60)).set_duration(audio_duration)
        bullet_clips.append(bullet)
    
    # Combine all elements
    slide = CompositeVideoClip([background, image.set_opacity(0.3), title_clip] + bullet_clips)
    return slide

def combine_slides_and_audio(video_clips, audio_paths):
    # Apply crossfade transition between video clips
    for j in range(1, len(video_clips)):
        video_clips[j] = video_clips[j].crossfadein(1)  # 1 second crossfade

    # Combine video clips
    final_video = concatenate_videoclips(video_clips, method="compose")
    
    # Combine audio files
    audio_clips = [AudioFileClip(audio_path) for audio_path in audio_paths]
    combined_audio = concatenate_audioclips(audio_clips)
    
    # Add audio to video
    final_video = final_video.set_audio(combined_audio)
    final_output_path = "output_videos/final_video_with_ai_slides_and_audio.mp4"
    os.makedirs('output_videos', exist_ok=True)
    final_video.write_videofile(final_output_path, codec="libx264", audio_codec="aac", fps=24)
    
    return final_output_path