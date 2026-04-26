import openai
import os
import dotenv

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def llm_response(prompt):
  response = openai.chat.completions.create(
    model = 'gpt-5.4-nano',
    messages = [{ 'role': 'user', 'content': prompt }],
    temperature = 0
  )

  return response.choices[0].message.content.strip()


# Define reviews
all_reviews = [
  'The mochi is excellent!',
  'Best soup dumplings I have ever eaten.',
  'Not worth the 3 month wait for a reservation.',
  'The colorful tablecloths made me smile!',
  'The pasta was cold.'
]


# In base of reviews, send to llm api and get sentiment of review (positive, negative)
all_sentiments = []
for review in all_reviews:
  prompt = f'''
    Classify the following review
    as having either a positive or
    negative sentiment. State your answer
    as a single word, either "positive" or
    "negative":

    {review}
  '''

  response = llm_response(prompt)

  all_sentiments.append(response)

print(all_sentiments)

# Count the sentiments

positive_sentiments = 0
negative_sentiments = 0

for sentiment in all_sentiments:
  if sentiment == 'positive':
    positive_sentiments = positive_sentiments + 1
  else: 
    negative_sentiments = negative_sentiments + 1

print(f'Positive sentiments: ', positive_sentiments)
print(f'Negative sentiments: ', negative_sentiments)