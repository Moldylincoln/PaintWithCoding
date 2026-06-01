import os
import requests
from dotenv import load_workbook, load_dotenv

load_dotenv()

api_key = os.getenv("POLLINATIONS_API_KEY")

if not api_key:
    raise ValueError("Missing POLLINATIONS_API_KEY environment variable.")

prompt = "cat"
url = f"https://gen.pollinations.ai/image/{prompt}"
headers = {"Authorization": f"Bearer {api_key}"}

print("Sending authorized request to Pollinations...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    with open("output_cat.jpg", "wb") as f:
        f.write(response.content)
    print("Success! Image saved to output_cat.jpg")
else:
    print(f"Failed with status code: {response.status_code}")
