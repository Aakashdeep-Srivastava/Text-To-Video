# services/gemini_service.py
import google.generativeai as genai
from config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_slide_content(text):
    prompt = f"""
    Given the following text, create content for a PowerPoint slide:
    "{text}"
    
    Please provide:
    1. A short, catchy title (max 5 words)
    2. 3 key points (each max 10 words)
    3. A relevant image search keyword (2-3 words)

    Format the response as follows:
    Title: [Your title here]
    Points:
    - [Point 1]
    - [Point 2]
    - [Point 3]
    Image keyword: [Your keyword here]
    """
    
    response = model.generate_content(prompt)
    return response.text.strip()

def parse_slide_content(content):
    lines = content.split('\n')
    title = lines[0].split(': ', 1)[1] if lines[0].startswith('Title:') else 'Slide Title'
    points = [line.strip('- ') for line in lines if line.startswith('- ')]
    image_keyword = lines[-1].split(': ', 1)[1] if lines[-1].startswith('Image keyword:') else 'abstract background'
    
    # Ensure we have at least 3 points
    while len(points) < 3:
        points.append("Additional information")
    
    return title, points, image_keyword