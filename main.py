import os
import io
import requests
from dotenv import load_dotenv
from PIL import Image
from flask import Flask

app = Flask(__name__)

def get_emoji_palette():
    return {
    # --- Original Base Colors & Fruits ---
        (255, 0, 0): "🟥",
        (255, 165, 0): "🟧",
        (255, 255, 0): "🟨",
        (255, 234, 192): "🥪",
        (0, 128, 0): "🟩",
        (0, 0, 255): "🟦",
        (128, 0, 128): "🟪",
        (165, 42, 42): "🟫",
        (0, 0, 0): "⬛",
        (125, 125, 125): "🩶",
        (255, 255, 255): "⬜",
        (220, 20, 60): "🍎",
        (50, 205, 50): "🍏",
        (255, 69, 0): "🍉",
        (255, 105, 180): "🍓",
        (139, 0, 0): "🍒",
        (255, 99, 71): "🍅",
        (255, 140, 0): "🍊",
        (244, 164, 96): "🍍",
        (255, 165, 79): "🍑",
        (255, 215, 0): "🍋",
        (255, 255, 0): "🍌",
        (154, 205, 50): "🍐",
        (144, 238, 144): "🍈",
        (186, 85, 211): "🍇",
        (218, 112, 214): "🫐",
        (210, 105, 30): "🥝",
        (210, 180, 140): "🥥",
        (107, 142, 35): "🫒",
        (128, 0, 32): "🥭",
    
        # --- Vegetables ---
        (34, 139, 34): "🥦",    # Broccoli (Dark Green)
        (0, 100, 0): "🥬",      # Leafy Green
        (85, 107, 47): "🫑",    # Bell Pepper (Green)
        (143, 188, 143): "🥒",  # Cucumber
        (46, 139, 87): "🫛",    # Pea Pod
        (255, 127, 80): "🥕",   # Carrot
        (218, 165, 32): "🌽",   # Corn
        (184, 134, 11): "🥔",   # Potato
        (205, 133, 63): "🍠",   # Sweet Potato
        (138, 43, 226): "🍆",   # Eggplant
        (216, 191, 216): "🧅",  # Onion
        (245, 245, 220): "🧄",  # Garlic
        (210, 180, 140): "🍄",  # Mushroom
    
        # --- Animals ---
        (255, 192, 203): "🐷",  # Pig Face (Pink)
        (255, 182, 193): "🦩",  # Flamingo (Light Pink)
        (240, 128, 128): "🐙",  # Octopus (Coral)
        (210, 105, 30): "🦧",   # Orangutan (Red-Brown)
        (244, 164, 96): "🦊",   # Fox (Sandy Orange)
        (255, 140, 0): "🐅",    # Tiger
        (255, 223, 0): "🐤",    # Baby Chick (Bright Yellow)
        (255, 215, 0): "🦁",    # Lion
        (173, 255, 47): "🪲",   # Beetle (Yellow-Green)
        (50, 205, 50): "🐸",    # Frog
        (0, 128, 128): "🦚",    # Peacock (Teal)
        (30, 144, 255): "🐋",   # Whale (Sky Blue)
        (0, 0, 139): "🐟",      # Fish (Deep Blue)
        (75, 0, 130): "👾",     # Alien Monster (Indigo)
        (147, 112, 219): "🪼",  # Jellyfish (Light Purple)
        (160, 82, 45): "🐻",    # Bear (Sienna Brown)
        (139, 69, 19): "🦫",    # Beaver (Dark Brown)
        (105, 105, 105): "🦏",  # Rhinoceros (Dim Gray)
        (169, 169, 169): "🐨",  # Koala (Dark Gray)
        (211, 211, 211): "🦭",  # Seal (Light Gray)
        (245, 245, 245): "🐑",  # Ewe (White)
    
        # --- Random / Objects / Nature ---
        (178, 34, 34): "🎈",    # Balloon (Firebrick Red)
        (255, 20, 147): "🎀",   # Ribbon (Deep Pink)
        (255, 160, 122): "salmon", # 🍣 Sushi
        (255, 69, 0): "🔥",     # Fire (Orange-Red)
        (255, 165, 0): "🎃",    # Jack-O-Lantern
        (238, 232, 170): "🧀",  # Cheese (Pale Goldenrod)
        (240, 230, 140): "🌟",  # Star (Khaki Yellow)
        (124, 252, 0): "🌱",    # Seedling (Lawn Green)
        (0, 250, 154): "🧪",    # Test Tube (Medium Spring Green)
        (0, 206, 209): "💎",    # Diamond (Dark Turquoise)
        (70, 130, 180): "💧",   # Droplet (Steel Blue)
        (65, 105, 225): "🌀",   # Cyclone (Royal Blue)
        (153, 50, 204): "🔮",   # Crystal Ball (Dark Orchid)
        (219, 112, 147): "🌺",  # Hibiscus (Pale Violet Red)
        (101, 67, 33): "💩",    # Pile of Poo (Dark Brown)
        (139, 115, 85): "🪵",   # Wood
        (112, 128, 144): "⚙️",   # Gear (Slate Gray)
        (192, 192, 192): "🪙",  # Coin (Silver)
        (248, 248, 255): "👻",  # Ghost (Ghost White)
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
headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

# The root route now handles general requests
@app.route('/')
def home():
    return "Welcome! Go to <b>/generate/your-prompt</b> in the URL bar to create emoji art."

# Dynamic route to accept any prompt directly from the web browser URL
@app.route('/generate/<user_prompt>')
def getEmojiGeneratedImage(user_prompt):
    print(f"Sending request to Pollinations for prompt: {user_prompt}...")
    
    # Using the official unified query string setup to ensure reliable string parsing
    base_url = "https://gen.pollinations.ai/image/"
    clean_url = f"{base_url}{user_prompt}"
    
    try:
        response = requests.get(clean_url, headers=headers)
        if response.status_code == 200:
            emoji_string = convert_image_to_emoji(response.content, output_width=125)
            return f"<pre style='font-family: monospace; line-height: 1; letter-spacing: 2px;'>{emoji_string}</pre>"
        else:
            return f"API Error: Received status code {response.status_code}", 400
    except Exception as e:
        return f"Connection Failed: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
