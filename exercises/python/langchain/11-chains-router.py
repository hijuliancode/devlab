# Objetivo: entender el Router Chain, donde el modelo decide
# a cuál subchain enviar el input según el tema de la pregunta

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv
import json

load_dotenv()

model = ChatOpenAI(model='gpt-5.4-nano', temperature=0.0)
parser = StrOutputParser()

# --- Subchains especializadas ---
# Cada una tiene un system prompt que la hace experta en un tema

physics_chain =(
  ChatPromptTemplate.from_messages([
    ("system", "You are an expert physics professor. Answer clearly and concisely."),
    ("human", "{input}")
  ])
  | model
  | parser
)

math_chain =(
  ChatPromptTemplate.from_messages([
    ("system", "You are an expert mathematician. Break down problems step by step."),
    ("human", "{input}")
  ])
  | model
  | parser
)

cs_chain =(
  ChatPromptTemplate.from_messages([
    ("system", "You are an expert software engineer. Give practical, clear answers."),
    ("human", "{input}")
  ])
  | model
  | parser
)

# Chain por defecto para preguntas que no encajan en ninguna categoría
default_chain =(
  ChatPromptTemplate.from_messages([
    ("system", "You are an expert __."),
    ("human", "{input}")
  ])
  | model
  | parser
)

# --- El Router ---
# Este prompt le dice al modelo cuáles son las opciones disponibles
# y le pide que decida cuál es la más apropiada para el input.
# El modelo no genera una respuesta a la pregunta aquí,
# solo decide a quién enviarla.

router_prompt = ChatPromptTemplate.from_template("""
Given the following question, decide wich specialist should answer it.
                                                 
Your options are:
- physics: for questions about physics, mechanics, thermodynamics, quantum, etc.
- math: for questions about mathematics, algebra, calculus, computers, etc.
- cs: for questions about programming, algorithms, software, computers, etc.
- default: for anything else that doesn't fit the above categories.
                                                 
Respond ONLY with a JSON object like this:
{{ "destination": "physics", "input": "the original question here" }}
                                                 
Question: {input}
""")

# El router es una chain que produce JSON con la desición
router_chain = router_prompt | model | parser


# --- La función que ejecuta el enrutamiento ---
# Recibe el JSON que produce el router, lo parsea,
# y ejecuta la subchain correcta según el destino elegido

def route(router_output: str) -> str:
  # Parseamos el JSON que el modelo generó
  try:
    decision = json.loads(router_output)
  except:
    # Si el modelo no responde en JSON válido, usamos la chain por defecto
    return default_chain.invoke({"input": router_output})
  
  destination = decision.get("destination", "default")
  question = decision.get("input", "")

  # Mapa de destinos a subchains

  chain_map = {
    "physics": physics_chain,
    "math": math_chain,
    "cs": cs_chain,
    "default": default_chain,
  }

  # Seleccionamos la subchain correcta, con default como fallback
  selected_chain = chain_map.get(destination, default_chain)

  print(f"Routing to: {destination}") # útil para ver la decisión del router
  return selected_chain.invoke({"input": question})


# --- La chain completa ---
# El input pasa por el router, luego RunnableLambda ejecuta
# la función route() que decide y llama a la subchain correcta
full_chain = router_chain | RunnableLambda(route)

# --- Pruebas ---
print("\n--- Question 1 ---")
print(full_chain.invoke({"input": "What is black body radiation?"}))

print("\n--- Question 2 ---")
print(full_chain.invoke({"input": "What is the time complexity of binary search?"}))

print("\n--- Question 3 ---")
print(full_chain.invoke({"input": "What is 2 + 2?"}))

print("\n--- Question 4 ---")
print(full_chain.invoke({"input": "Why does every cell contain DNA?"}))