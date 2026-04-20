import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def llm_response(prompt):
    response = openai.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [{ 'role': 'user', 'content': prompt }],
        temperature = 0
    )

    return response.choices[0].message.content.strip()


prompt = "What is the capital of France?"
response = llm_response(prompt)
print(response)

