import os
from moviepy.editor import ImageClip, concatenate_videoclips, CompositeVideoClip, AudioFileClip, concatenate_audioclips, TextClip, ColorClip
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

def create_slide(title, points, image_path, audio_file):
    # Define slide dimensions (16:9 aspect ratio)
    slide_width, slide_height = 1280, 720
    
    # Get audio duration
    audio_clip = AudioFileClip(audio_file)
    audio_duration = audio_clip.duration
    
    # Create a white background
    background = ColorClip(size=(slide_width, slide_height), color=(255, 255, 255)).set_duration(audio_duration)
    
    # Create title text
    title_clip = TextClip(title, fontsize=40, color='black', size=(slide_width - 80, None), 
                         method='caption', font='Arial-Bold')
    title_clip = title_clip.set_position(('center', 50)).set_duration(audio_duration)
    
    # Create bullet points
    bullet_clips = []
    max_y_position = 150  # Starting y-position for bullets
    
    for i, point in enumerate(points):
        bullet = TextClip(f"• {point}", fontsize=30, color='black', 
                         size=(slide_width - 100, None), method='caption', font='Arial')
        y_pos = max_y_position + i*60
        bullet = bullet.set_position((50, y_pos)).set_duration(audio_duration)
        bullet_clips.append(bullet)
        # Update max_y_position to include the height of this bullet point
        max_y_position = y_pos + bullet.h
    
    # Load and resize the image
    image = ImageClip(image_path)
    
    # Calculate image size (40% of slide width)
    target_width = int(slide_width * 0.4)
    aspect_ratio = image.h / image.w
    target_height = int(target_width * aspect_ratio)
    
    # Resize image
    image = image.resize(width=target_width)
    
    # Position image below text content with padding
    padding = 30
    image_y_position = max_y_position + padding
    
    # If image would go below slide, adjust size
    if image_y_position + target_height > slide_height:
        available_height = slide_height - image_y_position - padding
        scale_factor = available_height / target_height
        target_width = int(target_width * scale_factor)
        image = image.resize(width=target_width)
    
    image = image.set_position(('center', image_y_position)).set_duration(audio_duration)
    
    # Combine all elements (image is now on top, no opacity change)
    slide = CompositeVideoClip([background, title_clip] + bullet_clips + [image])
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