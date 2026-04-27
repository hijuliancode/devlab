import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI( model="gpt-5.4-nano", temperature=0.5)

respuesta1 = chat.invoke([HumanMessage(content='Hola, me llamo Julian')])

print(respuesta1.content)

respuesta2 = chat.invoke([HumanMessage(content='¿Cómo me llamo?')])

print(respuesta2.content)