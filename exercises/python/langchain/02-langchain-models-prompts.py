import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI(
  model="gpt-5.4-nano",
  temperature=0.5,
)

template_string = """Translate the text \
that is delimited by triple backticks \
into a style that is {style}. \
text: ```{text}```
"""

prompt_template = ChatPromptTemplate.from_template(template_string)

customer_style = """Spanish pirate \
in a calm and polite tone, with a touch of humor.
"""

customer_email = """Arrr, I be fuming that me blender lid \
flew off and splattered me kitchen walls \
with smoothie! And to make matters worse, \
the warranty don't cover the cost of \
cleaning up me kitchen. I need yer help \
right now, matey!
"""

customer_messages = prompt_template.format_messages(
  style=customer_style,
  text=customer_email,
)

customer_response = chat.invoke(customer_messages)

print(customer_response.content)
print("\n\n") # Add some space between the two responses

service_reply = """Hey there customer, \
the warranty does not cover \
cleaning expenses for your kitchen \
because it's your fault that \
you misused your blender \
by forgetting to put the lid on before \
starting the blender. \
Tough luck, See ya!
"""

service_style_pirate = """\
a polite tome \
that speaks in Spanish pirate
"""

service_messages = prompt_template.format_messages(
  style=service_style_pirate,
  text=service_reply,
)

print(chat.invoke(service_messages).content)
