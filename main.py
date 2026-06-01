import os
import io  
import requests
from dotenv import load_dotenv
from PIL import Image
from flask import Flask

app = Flask(__name__)

def get_emoji_palette():
    return {
        (255, 0, 0): "🔴",
        (255, 165, 0): "🟠",
        (255, 255, 0): "🟡",
        (0, 128, 0): "🟢",
        (0, 0, 255): "🔵",
        (128, 0, 128): "🟣",
        (165, 42, 42): "🟤",
        (0, 0, 0): "⚫",
        (255, 255, 255): "⚪",
    }

def find_closest_emoji(pixel, palette):
    r, g, b = pixel[:3]
    closest_emoji = "⚫"
    min_distance = float('inf')
    for color, emoji_char in palette.items():
        distance = (r - color[0])**2 + (g - color[1])**2 + (b - color[2])**2
        if distance < min_distance:
            min_distance = distance
            closest_emoji = emoji_char
    return closest_emoji

def convert_image_to_emoji(image_bytes, output_width=40):
    try:
        img = Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        return f"Error processing image: {str(e)}"
        
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

prompt = "cat"
url = f"https://pollinations.ai{prompt}"
headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

@app.route('/')
def getEmojiGeneratedImage():
    print("Sending request to Pollinations...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        with open("output_cat.jpg", "wb") as f:
            f.write(response.content)
            
        emoji_string = convert_image_to_emoji(response.content, output_width=30)
        return f"<pre style='font-family: monospace; line-height: 1; letter-spacing: 2px;'>{emoji_string}</pre>"
    else:
        return f"Failed with status code: {response.status_code}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
