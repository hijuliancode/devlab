# Objetivo: entender qué es un agente y cómo el modelo toma decisiones
# usando herramientas disponibles siguiendo el patrón ReAct.
# Un agente no sigue pasos predefinidos, decide en tiempo de ejecución.

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import PromptTemplate
from datetime import date
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model='gpt-5.4-nano', temperature=0.0)


# --- Herramienta 1: Search (herramienta predefinida de LangChain) ---

# LangChain tiene herramientas ya construidas para servicios comunes
# Solo necesitamos instanciarlas y el agente sabra cuando usarlas


search = DuckDuckGoSearchRun()

# --- Herramienta 2: fecha actual (herramienta personalizada) ---

# El decorador @tool convierte cualquier función de python en una herramienta.
# El docstring es critico, es lo que el modelo lee para saber si usarla
@tool
def get_today_date(text: str) -> str:
    """Returns today's date in YYYY-MM-DD format.
    Use this tool for any question about the current date or today's date.
    The input should always be an empty string."""

    return str(date.today())


# --- Herramienta 3: calculadora personalizada ---

# Otra herramienta customo para mostrar que podemos conectar cualquier función.

@tool
def calculate(expression: str) -> str:
    """Evaluates a mathematical expression and returns the result.
    Use this for any math calculation.
    Input should be a valid Python math expression like '25 * 4' or '100 / 3'."""

    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error calculating {e}"
    

# Lista de herramientas disponibles para el agente
tools = [search, get_today_date, calculate]

# --- El prompt del agente ---
# Este prompt le dice al agente como debe comportarse y como usar
# el formato ReAct (Thought, Action, Observation).

prompt = PromptTemplate.from_template("""
Answer the following questions as best you can. 
You have acces to the following tools:

{tools}

Using the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}

""")

# --- Creamos el agente y el executor ---
# El agente contiene logica de razonamiento (el modelo + el prompt).
# El executor es el loop que ejecuta el ciclo ReAct hasta llegar al Final Answer.

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="You are a helpful assistant. Use the available tools to answer questions accurately."
)


# --- Pruebas ---
# Puedo observar en el output cómo el modelo razona y elige qué herramienta usar

print("\n--- Pregunta 1: fecha ---")
result = agent.invoke({"messages": [{"role": "user", "content": "What is today's date?"}]})
print("Final:", result["messages"][-1].content)

print("\n--- Pregunta 2: cálculo ---")
result = agent.invoke({"messages": [{"role": "user", "content": "What is 25% of 348?"}]})
print("Final:", result["messages"][-1].content)

print("\n--- Pregunta 3: búsqueda ---")
result = agent.invoke({"messages": [{"role": "user", "content": "Who is Alan Turing and what is he known for?"}]})
print("Final:", result["messages"][-1].content)

print("\n--- Pregunta 4: combinada ---")
result = agent.invoke({"messages": [{"role": "user", "content": "What year was Python programming language created, and how many years ago was that from today?"}]})
print("Final:", result["messages"][-1].content)

print("\n--- Mensajes internos de la pregunta 4 ---")
for msg in result["messages"]:
    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        for tc in msg.tool_calls:
            print(f"AIMessage llamó herramienta: {tc['name']} con input: {tc['args']}")
    else:
        print(f"{type(msg).__name__}: {msg.content[:150] if msg.content else ''}")


print("\n--- Pregunta 5: búsqueda forzada ---")
result = agent.invoke({
    "messages": [{"role": "user", "content": "What is the current price of Apple stock today?"}]
})
print("Final:", result["messages"][-1].content)

print("\n--- Mensajes internos de la pregunta 5 ---")
for msg in result["messages"]:
    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        for tc in msg.tool_calls:
            print(f"AIMessage llamó herramienta: {tc['name']} con input: {tc['args']}")
    else:
        print(f"{type(msg).__name__}: {msg.content[:150] if msg.content else ''}")