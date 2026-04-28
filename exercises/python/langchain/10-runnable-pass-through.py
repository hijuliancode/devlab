from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model='gpt-5.4-nano', temperature=0.0)
parser = StrOutputParser()

prompt_name = ChatPromptTemplate.from_template(
  "What is the best name to describe a company that makes {product}? "
  "Return only the name."
)

prompt_description = ChatPromptTemplate.from_template(
  "Write a 20 word description for the following company name: {company_name}"
)

# chain que solo genera el nombre
chain_name = prompt_name | model | parser

# chain que solo genera la descipción, recibe company_name como input
chain_description = prompt_description | model | parser

# RunnablePassthrough.assign() acumula resultados en un diccionario.
# Primero agrega "company_name" ejecutando chain_name
# Luego agrega "description" ejecutando chain_description con lo que ya tiene.
# Al final tenemos acceso a ambos resultados sin perder ninguno.

chain = RunnablePassthrough.assign(
  company_name=chain_name
) | RunnablePassthrough.assign(
  description=chain_description
)

result = chain.invoke({"product": "the project management tool for your agency"})

# Ahora tienes ambos valores separados y los formateas como quieras
print(f"Company name: {result['company_name']}")
print(f"Company name: {result['description']}")