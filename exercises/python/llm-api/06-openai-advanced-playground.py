import openai
from dotenv import load_dotenv
import os

load_dotenv()

client = openai.OpenAI()

def get_completion(prompt, model='gpt-3.5-turbo'):
  messages = [{"role": "user", "content": prompt}]
  response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0.0,  # adjust the creativity of the response
  )

  return response.choices[0].message.content

# print(get_completion("What is the capital of France?"))
# print(get_completion("What is 1 + 1?"))

customer_email = """
Arrr, I be fuming that me blender lid \\
flew off and splattered me kitchen walls \\
with smoothie! And to make matters worse, \\
the warranty don't cover the cost of \\
cleaning up me kitchen. I need yer help \\
right now, matey!
"""

style = """Spanish \\
in a calm and polite tone, with a touch of humor.
"""

prompt = f"""Translate the text \\ 
that is delimited by triple backticks
into a style that is {style}.
text: ```{customer_email}```
"""

print(get_completion(prompt))
