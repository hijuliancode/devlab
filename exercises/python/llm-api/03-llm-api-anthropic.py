import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('ANTHROPIC_API_KEY')

client = anthropic.Anthropic(api_key=api_key)

message = client.messages.create(
  model = "claude-haiku-4-5",
  max_tokens = 200,
  messages = [
    {
      "role": "user",
      "content": "Cual es la capital de Colombia?",
    }
  ],
)


print(message.content[0].text)