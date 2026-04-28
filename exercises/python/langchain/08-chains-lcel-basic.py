# Objetivo: replicar el ejercicio anterior pero usando un chain con LCEL
# COmparar la diferencia con el glue code del ejercicio anterior

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model='gpt-5.4-nano', temperature=0.0)
parser = StrOutputParser()

# Los prompts son exactamente iguales al ejercicio anterior
# La diferencia esta en como los conectamos
prompt_name = ChatPromptTemplate.from_template(
  "What is the best name to describe a company that makes {product}? "
  "Return only the name."
)

# Esto es una chain básica: prompt | model | parser
# El operador | conecta las piezas: la salida de cada una entra a la siguiente
# No hay glue code, no hay variables intermedias, no hay .content manual
chain_name = prompt_name | model | parser

# Una sola línea reemplaza los 4 pasos manuales del ejercicio anterior
result = chain_name.invoke({"product": "Queen Size Sheet Set"})

print(f"Company name: {result}")