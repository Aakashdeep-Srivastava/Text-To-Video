# utils/image_utils.py
import os
from PIL import Image

def resize_image(image_path, target_width, target_height):
    with Image.open(image_path) as img:
        # Calculate aspect ratios
        img_aspect = img.width / img.height
        target_aspect = target_width / target_height
        
        if img_aspect > target_aspect:
            # Image is wider, crop the sides
            new_width = int(target_aspect * img.height)
            left = (img.width - new_width) // 2
            img = img.crop((left, 0, left + new_width, img.height))
        else:
            # Image is taller, crop the top and bottom
            new_height = int(img.width / target_aspect)
            top = (img.height - new_height) // 2
            img = img.crop((0, top, img.width, top + new_height))
        
        # Resize to target dimensions
        img = img.resize((target_width, target_height), Image.LANCZOS)
        
        # Save the resized image
        resized_path = f"{os.path.splitext(image_path)[0]}_resized.jpg"
        img.save(resized_path, "JPEG", quality=95)
        return resized_path