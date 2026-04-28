# objectivo: entender por qué necesitamos chains viendo el problema sin ellas

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model='gpt-5.4-nano', temperature=0.0)
parser = StrOutputParser()

# --- Paso 1: generar el nombre de una empresa ---

prompt_name = ChatPromptTemplate.from_template("""\
What is the best name to describe a company that makes {product}? 

Return only the name.
""")

# Ejecuto el primer paso manualmente
messages_name = prompt_name.format_messages(product="Queen Size Sheet Set")
response_name = model.invoke(messages_name)
business_name = parser.parse(response_name.content)

print(f"Nombre generado: {business_name}")


# --- Paso 2: generar descripción usando el resultado del paso 1 ---
# Nota: tenemso que pasar manualmente el resultado de arriba al siguiente prompt
# Esto es exactamente el "glue code" que menciona Andrew NG en la introducción

prompt_description = ChatPromptTemplate.from_template(
  "Write a 20 word description for the following company: {company_name}"
)

messages_description = prompt_description.format_messages(company_name=business_name)
response_description = model.invoke(messages_description)
business_description = parser.parse(response_description.content)

print(f"Descripción: {business_description}")