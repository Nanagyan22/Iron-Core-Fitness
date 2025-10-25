from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

genai.api_key = os.environ.get("GEMINI_API_KEY")  # Must be set in .env

response = genai.generate_text(
    model="gemini-2.5-flash",
    prompt="Hello world!",
    temperature=0.3,
)
print(response.text)
