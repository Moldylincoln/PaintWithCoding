import os
import io
import requests
from dotenv import load_dotenv
from PIL import Image
from flask import Flask

app = Flask(__name__)

def get_emoji_palette():
    return {
        # ==========================================
        # RED / DARK RED / CRIMSON / CORAL
        # ==========================================
        (255, 0, 0): "🟥",      # Red Square
        (139, 0, 0): "🍒",      # Cherries (Dark Red)
        (178, 34, 34): "🎈",    # Balloon (Firebrick)
        (220, 20, 60): "🍎",    # Red Apple
        (255, 99, 71): "🍅",    # Tomato (Light Red)
        (240, 128, 128): "🐙",  # Octopus (Coral Red)
        (255, 69, 0): "🔥",     # Fire (Orange-Red)
        (128, 0, 0): "🧯",      # Fire Extinguisher (Maroon)
        (165, 0, 33): "🪓",      # Axe (Deep Crimson)
        (194, 24, 7): "🥊",     # Boxing Glove
        (141, 16, 16): "🥀",     # Withered Flower
        (214, 40, 40): "🌶️",     # Hot Pepper
        (186, 12, 47): "🎒",     # School Backpack
        (156, 10, 10): "📮",     # Postbox
        
        # ==========================================
        # PINK / DEEP PINK / ROSE / MAGENTA
        # ==========================================
        (255, 192, 203): "🐷",  # Pig Face (Light Pink)
        (255, 182, 193): "🦩",  # Flamingo
        (255, 105, 180): "🍓",  # Strawberry
        (255, 20, 147): "🎀",   # Ribbon (Deep Pink)
        (219, 112, 147): "🌺",  # Hibiscus
        (255, 130, 171): "🌸",  # Cherry Blossom
        (241, 156, 187): "🧠",  # Brain
        (255, 110, 180): "💕",  # Two Hearts
        (234, 76, 137): "💗",   # Growing Heart
        (199, 21, 133): "🪕",   # Banjo (Deep Magenta accent)
    
        # ==========================================
        # ORANGE / TANGERINE / PEACH / AMBER
        # ==========================================
        (255, 165, 0): "🟧",    # Orange Square
        (255, 140, 0): "🍊",    # Tangerine
        (244, 164, 96): "🦊",   # Fox Face (Sandy Orange)
        (255, 165, 79): "🍑",   # Peach
        (255, 127, 80): "🥕",   # Carrot
        (128, 0, 32): "🥭",     # Mango
        (204, 85, 0): "🧱",     # Brick
        (226, 88, 34): "🏀",    # Basketball
        (255, 117, 24): "🎃",   # Jack-O-Lantern
        (230, 92, 0): "🦺",     # Safety Vest
        (242, 133, 0): "🦊",    # Fox
        (213, 94, 0): "🍤 fried shrimp", # Fried Shrimp
    
        # ==========================================
        # YELLOW / GOLD / MUSTARD / CREAM
        # ==========================================
        (255, 255, 0): "🟨",    # Yellow Square
        (255, 215, 0): "🍋",    # Lemon (Gold)
        (244, 164, 96): "🍍",   # Pineapple
        (255, 223, 0): "🐤",    # Baby Chick
        (218, 165, 32): "🌽",   # Corn
        (238, 232, 170): "🧀",  # Cheese
        (240, 230, 140): "🌟",  # Star
        (255, 234, 192): "🥪",  # Sandwich (Cream/Beige)
        (253, 222, 85): "🍌",   # Banana
        (255, 191, 0): "👑",    # Crown
        (245, 222, 179): "🥞",  # Pancakes
        (255, 239, 148): "🌕",  # Full Moon
        (250, 218, 94): "🍯",   # Honey Pot
        (225, 193, 7): "🚕",    # Taxi
    
        # ==========================================
        # GREEN / LIME / EMERALD / OLIVE / FOREST
        # ==========================================
        (0, 128, 0): "🟩",      # Green Square
        (50, 205, 50): "🍏",    # Green Apple
        (34, 139, 34): "🥦",    # Broccoli (Forest Green)
        (0, 100, 0): "🥬",      # Leafy Green (Dark Green)
        (85, 107, 47): "🫑",    # Green Bell Pepper
        (143, 188, 143): "🥒",  # Cucumber
        (46, 139, 87): "🫛",    # Pea Pod
        (107, 142, 35): "🫒",   # Olive
        (124, 252, 0): "🌱",    # Seedling (Lawn Green)
        (0, 250, 154): "🧪",    # Test Tube (Spring Green)
        (173, 255, 47): "🪲",   # Beetle (Lime Green)
        (0, 255, 0): "🦎",      # Lizard
        (60, 179, 113): "🌲",   # Evergreen Tree
        (154, 205, 50): "🍐",   # Pear
        (144, 238, 144): "🍈",  # Melon
        (40, 167, 69): "💵",    # Dollar Bill
        (10, 90, 30): "🛕",     # Hindu Temple (Moss Green)
        (139, 195, 74): "🐢",   # Turtle
    
        # ==========================================
        # TEAL / CYAN / TURQUOISE / LIGHT BLUE
        # ==========================================
        (0, 206, 209): "💎",    # Diamond (Turquoise)
        (0, 128, 128): "🦚",    # Peacock (Teal)
        (173, 216, 230): "💧",  # Droplet (Light Blue)
        (30, 144, 255): "🐋",   # Whale (Sky Blue)
        (135, 206, 235): "👕",  # T-Shirt (Sky Blue)
        (0, 191, 255): "🥶",    # Cold Face
        (72, 209, 204): "🩱",   # One-Piece Swimsuit
    
        # ==========================================
        # BLUE / DEEP BLUE / NAVY / INDIGO
        # ==========================================
        (0, 0, 255): "🟦",      # Blue Square
        (0, 0, 139): "🐟",      # Fish (Deep Blue)
        (65, 105, 225): "🌀",   # Cyclone
        (70, 130, 180): "👖",   # Jeans (Steel Blue)
        (25, 25, 112): "🌌",    # Milky Way (Midnight Navy)
        (16, 44, 87): "📘",     # Blue Book
        (10, 50, 120): "🗳️",    # Ballot Box
        (58, 125, 211): "🧢",   # Blue Cap
    
        # ==========================================
        # PURPLE / VIOLET / AMETHYST / PLUM
        # ==========================================
        (128, 0, 128): "🟪",    # Purple Square
        (186, 85, 211): "🍇",   # Grapes
        (218, 112, 214): "🫐",  # Blueberries (Indigo-Purple)
        (138, 43, 226): "🍆",   # Eggplant
        (75, 0, 130): "👾",     # Alien Monster (Indigo)
        (147, 112, 219): "🪼",  # Jellyfish (Light Violet)
        (153, 50, 204): "🔮",   # Crystal Ball
        (106, 13, 173): "😈",   # Devil Face
        (139, 100, 234): "🛜",  # Wireless
        (230, 230, 250): "🪻",  # Hyacinth (Lavender)
        (74, 20, 140): "🪯",    # Khanda
    
        # ==========================================
        # BROWN / TAN / BEIGE / COCOA / WOOD
        # ==========================================
        (165, 42, 42): "🟫",    # Brown Square
        (210, 180, 140): "🥥",  # Coconut / Tan
        (184, 134, 11): "🥔",   # Potato
        (205, 133, 63): "🍠",   # Sweet Potato
        (210, 105, 30): "🦧",   # Orangutan (Red-Brown)
        (160, 82, 45): "🐻",    # Bear (Sienna)
        (139, 69, 19): "🦫",    # Beaver (Dark Brown)
        (101, 67, 33): "💩",    # Pile of Poo
        (139, 115, 85): "🪵",   # Wood Log
        (222, 184, 135): "🍞",  # Bread (Burlywood)
        (110, 44, 0): "🍫",     # Chocolate Bar
        (141, 110, 99): "🦘",   # Kangaroo
        (93, 64, 55): "🥾",     # Hiking Boot
        (78, 52, 46): "☕",     # Hot Beverage / Coffee
    
        # ==========================================
        # GREY / SILVER / SLATE / CHARCOAL
        # ==========================================
        (125, 125, 125): "🩶",  # Grey Heart
        (105, 105, 105): "🦏",  # Rhinoceros (Dim Grey)
        (169, 169, 169): "🐨",  # Koala
        (112, 128, 144): "⚙️",   # Gear (Slate Grey)
        (192, 192, 192): "🪙",  # Coin (Silver)
        (80, 80, 80): "🔩",     # Nut and Bolt (Iron Grey)
        (150, 150, 150): "📎",  # Paperclip
        (200, 200, 200): "🥄",  # Spoon
        (50, 50, 50): "🪨",     # Rock (Dark Charcoal)
    
        # ==========================================
        # WHITE / LIGHT / OFF-WHITE / GHOST
        # ==========================================
        (255, 255, 255): "⬜",  # White Square
        (245, 245, 220): "🧄",  # Garlic
        (211, 211, 211): "🦭",  # Seal (Light Grey)
        (245, 245, 245): "🐑",  # Ewe (White Wool)
        (248, 248, 255): "👻",  # Ghost
        (255, 250, 250): "🥛",  # Glass of Milk
        (240, 248, 255): "🍚",  # Cooked Rice
        (255, 255, 240): "🧻",  # Roll of Paper
        (245, 245, 245): "🥼",  # Lab Coat
    
        # ==========================================
        # BLACK / MIDNIGHT / DARK OBSIDIAN
        # ==========================================
        (0, 0, 0): "⬛",        # Black Square
        (20, 20, 20): "💣",     # Bomb
        (15, 15, 15): "🕶️",      # Sunglasses
        (5, 5, 5): "🎩",        # Top Hat
        (30, 30, 30): "🪰",     # Fly
        (10, 10, 10): "🎱",     # 8-Ball
        (25, 25, 25): "🖤",     # Black Heart
        (1, 1, 1): "🐈‍⬛",       # Black Cat
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
            emoji_string = convert_image_to_emoji(response.content, output_width=175)
            return f"<pre style='font-family: monospace; line-height: 1; letter-spacing: 2px;'>{emoji_string}</pre>"
        else:
            return f"API Error: Received status code {response.status_code}", 400
    except Exception as e:
        return f"Connection Failed: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
