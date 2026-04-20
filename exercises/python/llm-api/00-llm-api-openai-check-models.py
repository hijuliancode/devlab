import openai
import os
import dotenv

dotenv.load_dotenv()

client = openai.OpenAI()

models = client.models.list()

for model in models.data:
  print(model.id)