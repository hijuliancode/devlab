import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
  raise ValueError('Missing GEMINI_API_KEY in .env')

client = genai.Client(api_key=api_key)

try:

  response = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents = "Cual es la capital de Colombia",
  )

  print(response.text)

except Exception as error:
  print(f'Gemini request failed: {error}')