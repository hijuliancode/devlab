import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI(model='gpt-5.4-nano', temperature=0.0)

# Esta lista es nuestra "memoria manual"
# Es exactamente lo que hace langchain internamente
history = [
  SystemMessage(content="Eres un asistente amigable, gracioso y conciso.")
]

def conversar(user_message):
  # Agregamos el mensaje del usuario al historial
  history.append(HumanMessage(content=user_message))

  # Enviamos 'todo' el historial al modelo, no solo el ultimo mensaje
  response = chat.invoke(history)

  # Guardamos la respuesta del modelo también
  history.append(AIMessage(content=response.content))

  return response.content

# Probar la conversación
print(conversar('Hola, me llamo Julian'))
print(conversar('Cual es la capital de Italia'))
print(conversar('¿Recuerdas mi nombre?'))
print(conversar('Cuantos mensajes llevamos en esta conversación'))