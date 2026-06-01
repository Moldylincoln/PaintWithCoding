import os
import requests
from dotenv import load_workbook, load_dotenv
from PIL import Image
from flask import Flask

app = Flask(__name__)
                                 
def get_emoji_palette():
    """Defines a map of RGB colors to corresponding emojis."""
    return {
        (255, 0, 0): "🔴",      # Red
        (255, 165, 0): "🟠",    # Orange
        (255, 255, 0): "🟡",    # Yellow
        (0, 128, 0): "🟢",      # Green
        (0, 0, 255): "🔵",      # Blue
        (128, 0, 128): "🟣",    # Purple
        (165, 42, 42): "🟤",    # Brown
        (0, 0, 0): "⚫",        # Black
        (255, 255, 255): "⚪",  # White
    }

def find_closest_emoji(pixel, palette):
    """Calculates Euclidean distance to find the closest color match."""
    r, g, b = pixel[:3]
    closest_emoji = "⚫"
    min_distance = float('inf')
    
    for color, emoji_char in palette.items():
        # Distance formula: √((r2-r1)² + (g2-g1)² + (b2-b1)²)
        distance = (r - color[0])**2 + (g - color[1])**2 + (b - color[2])**2
        if distance < min_distance:
            min_distance = distance
            closest_emoji = emoji_char
            
    return closest_emoji

def convert_image_to_emoji(image_path, output_width=40):
    """Resizes image and prints out the emoji representation."""
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return

    w_percent = (output_width / float(img.size[0]))
    output_height = int((float(img.size[1]) * float(w_percent)))
    
    img = img.resize((output_width, output_height), Image.Resampling.BILINEAR)
    img = img.convert('RGB')
    
    palette = get_emoji_palette()
    emoji_art = []
    
    for y in range(output_height):
        row_str = ""
        for x in range(output_width):
            pixel = img.getpixel((x, y))
            row_str += find_closest_emoji(pixel, palette)
        emoji_art.append(row_str)
        
    return "\n".join(emoji_art)

load_dotenv()

api_key = os.environ.get("POLLINATIONS_API_KEY")

if not api_key:
    raise ValueError("Missing POLLINATIONS_API_KEY environment variable.")

prompt = "cat"
url = f"https://gen.pollinations.ai/image/{prompt}"
headers = {"Authorization": f"Bearer {api_key}"}

@app.route('/')
def getEmojiGeneratedImage():
print("Sending authorized request to Pollinations...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    with open("output_cat.jpg", "wb") as f:
        return convert_image_to_emoji(response.content, output_width=30)
    print("Success! Image saved to output_cat.jpg")
else:
    print(f"Failed with status code: {response.status_code}")
    
app.run(host='0.0.0.0', port=8080)
