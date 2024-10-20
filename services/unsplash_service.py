# services/unsplash_service.py
import requests
import os
from config import UNSPLASH_URL, UNSPLASH_ACCESS_KEY

def fetch_photo(query):
    if not query.strip():
        query = "abstract background"
    
    headers = {
        'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'
    }
    params = {
        'query': query,
        'page': 1,
        'per_page': 1,
        'orientation': 'landscape'
    }
    response = requests.get(UNSPLASH_URL, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    results = response.json()['results']
    if results:
        return results[0]
    else:
        raise ValueError(f"No photos found for the query: {query}")

def save_photo(photo_url, photo_id):
    response = requests.get(photo_url, timeout=10)
    response.raise_for_status()
    os.makedirs('images', exist_ok=True)
    with open(f'images/{photo_id}.jpg', 'wb') as file:
        file.write(response.content)
    return f'images/{photo_id}.jpg'

def fetch_and_save_photo(image_keyword):
    photo = fetch_photo(image_keyword)
    photo_url = photo['urls']['regular']
    photo_id = photo['id']
    return save_photo(photo_url, photo_id)