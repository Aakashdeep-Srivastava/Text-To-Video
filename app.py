import streamlit as st
import asyncio
import logging
import os
from PIL import Image
from utils.image_utils import resize_image
from utils.audio_utils import text_to_speech
from utils.video_utils import create_slide, combine_slides_and_audio
from services.unsplash_service import fetch_and_save_photo
from services.gemini_service import generate_slide_content, parse_slide_content
from utils.avatar_utils import generate_avatar_animation
# Ensure ImageMagick is properly configured
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "ImageMagick-7.1.1-Q16-HDRI\magick.exe"})  # Replace with your actual path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

VOICES = [
    'Elon Musk', 'Narendra Modi', 'HC Verma'
]
def load_image(image_path):
    try:
        return Image.open(image_path)
    except Exception as e:
        st.warning(f"Failed to load image from {image_path}. Error: {e}")
        return None

def main():
    st.set_page_config(layout="wide")

    # Sidebar
    with st.sidebar:
        # Try to load the logo image
        logo_path = os.path.join("assets", "logo.png")
        logo_image = load_image(logo_path)
        
        if logo_image:
            st.image(logo_image, width=200)
        else:
            st.write("Logo not found. Please check the image path.")

       
        selected_voice = st.selectbox("Select a voice:", VOICES)

        # AI Avatar
        #st.subheader("Professor Proton")
        avatar_placeholder = st.empty()
        
        if 'audio_paths' in st.session_state:
            # Generate and display avatar animation
            avatar_animation = generate_avatar_animation(st.session_state['audio_paths'])
            avatar_placeholder.image(avatar_animation, use_column_width=True)

        st.subheader("Professor Proton")
    # Main content area
    st.title("AI Video Generator")
    st.subheader("Enter your text")
    user_input = st.text_area("", height=50)
    
    if st.button("Generate Video"):
        if user_input:
            with st.spinner("Generating video..."):
                try:
                    sentences = [s.strip() for s in user_input.split('.') if s.strip()]
                    video_clips = []
                    audio_paths = []
                    
                    for sentence in sentences:
                        slide_content = generate_slide_content(sentence)
                        title, points, image_keyword = parse_slide_content(slide_content)
                        
                        try:
                            image_path = fetch_and_save_photo(image_keyword)
                        except Exception as e:
                            st.warning(f"Error fetching image: {e}. Using a default background.")
                            image_path = os.path.join("assets", "default_background.jpg")
                        
                        audio_file = asyncio.run(text_to_speech(sentence, voice='en-US-AriaNeural'))
                        audio_paths.append(audio_file)
                        
                        slide = create_slide(title, points, image_path, audio_file)
                        video_clips.append(slide)
                    
                    final_output_path = combine_slides_and_audio(video_clips, audio_paths)
                    
                    st.session_state['video_path'] = final_output_path
                    st.session_state['audio_paths'] = audio_paths
                    st.success("Video generated successfully!")
                
                except Exception as e:
                    st.error(f"Error generating video: {e}")

    # Display generated video
    if 'video_path' in st.session_state:
        st.subheader("Generated Video")
        video_file = open(st.session_state['video_path'], 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)

if __name__ == "__main__":
    main()