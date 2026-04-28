# Objectivo: Encadenar dos pasos donde la salida del primero
# alimenta automáticamente al segundo, sin glue code manual

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-5.4-nano", temperature=0.0)
parser = StrOutputParser()

# Prompt 1: genera el nombre de la empresa
prompt_name = ChatPromptTemplate.from_template(
  "What is the best name to describe a company that makes {product}? "
  "Return only the name."
)

# Prompt 1: genera la descripción usando el nombre generado por el prompt 1
prompt_description = ChatPromptTemplate.from_template(
  "Write a 20 word description for the following company name: {company_name}"
)

# Aquí seta lo interesante: la lambda transforma el string que produce
# el primer paso en el diccionario que espera el segundo prompt.
# Sin esto, el segundo prompt no sabría a qué variable asignar el string

chain = (
  prompt_name
  | model
  | parser
  | (lambda name: {"company_name": name}) # puente entre los dos pasos
  | prompt_description
  | model
  | parser
)

# Una sola llamada ejecuta los 4 pasos en secuencia
result = chain.invoke({"product": "Play chess online for free with over 250 million members from around the world. Have fun playing with friends or challenging the computer!"})

print(f"Final description: {result}")
