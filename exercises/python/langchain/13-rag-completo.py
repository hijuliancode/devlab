# Objetivo: construir un pipeline RAG completo con código moderno.
# RAG = Retrieval-Augmented Generation
# En vez de enviarle al modelo todo el conocimiento, primero buscamos
# lo relevante y solo eso le enviamos

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model='gpt-5.4-nano', temperature=0.0)
embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small')
parser = StrOutputParser()

# --- Fase 1: Indexación ---
# Aquí simulamos tener un catálogo de productos deportivos
# En producción estos datos vienen de bases de datos

documents = [
  Document(page_content="The ProRunner X5 shoe features advanced cushioning and carbon fiber plate for marathon runners. Ideal for athletes focused on speed and endurance."),
  Document(page_content="AquaSwift goggles provide UV protection and anti-fog coating. Designed for competitive swimmers training in outdoor pools."),
  Document(page_content="FlexPro resistance bands set includes 5 levels from light to heavy. Used for strength training, rehabilitation, and warm-up routines."),
  Document(page_content="VeloMax cycling helmet with aerodynamic design and ventilation system. Recommended for road cyclists and triathletes."),
  Document(page_content="CoreBalance yoga mat with alignment lines and extra thickness for joint protection. Popular among yoga and pilates instructors."),
  Document(page_content="StrikeForce boxing gloves with shock-absorbing foam. Used by amateur and professional boxers for sparring and bag work."),
  Document(page_content="SpeedRope jump rope with ball bearings for smooth rotation. Used in HIIT training and boxing conditioning workouts."),
]

# Creamos el vector store y le agregamos los documentos
# Internamente esto genera un embedding por cada documento y los guarda.
# Esta es la fase costosa que en producción hacemos una sola vez
vector_store = InMemoryVectorStore(embeddings_model)
vector_store.add_documents(documents=documents)

print("Fase de indexación completa. Los documentos están en el vector store.")

# --- Fase 2: Búsqueda por similitud (para entender qué hace el retriever) ---
# Hacemos una búsqueda manual para ver qué documentos encuentra
# El retriever convierte la pregunta en un embedding y busca los más similares.

test_query = "I need equipment for water sports"
relevant_docs = vector_store.similarity_search(test_query, k=2)

print(f"\nBúsqueda de prueba: '{test_query}'")
print("\nDocumentos más relevantes encontrados:")
for i, doc in enumerate(relevant_docs):
  print(f"  {i+1}. {doc.page_content[:80]}...")

# --- Fase 3: Pipeline RAG completo ---
# Aquí conectamos el retriever con el modelo usando LCEL
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# Este prompt le dice al modelo que responda SOLO basándose en el contexto
# que le damos. Esto evita que el modelo "invente" información.
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful sports equipment assistant.
Answer the question based ONLY on the following context.
If the answer is not in the context, say 'I don't have information about that.'

Context: {context}"""),
    ("human", "{question}")
])

# Esta función toma los documentos recuperados y los une en un solo texto
# para enviarselos al modelo en el prompt. Es el método "stuff"
def format_docs(docs):
  return "\n\n".join(doc.page_content for doc in docs)

# La chain completa:
# 1. El retriever busca documentos relevantes en base a la pregunta
# 2. format_docs los convierte en texto
# 3. RunnablePassThroug pasa la pregunta original sin cambios
# 4. El prompt arma el mensaje con el contexto y la pregunta
# 5. El modelo genera la respuesta
# 6. El parser la convierte en string limpio

rag_chain = (
  {
    "context": retriever | format_docs, # busca docs y los formatea
    "question": RunnablePassthrough() # pasa la pregunta tal cual
  }
  | prompt
  | model
  | parser
)

# --- Pruebas ---
print("\n--- RAG en acción ---")

queries = [
    "What equipment is good for swimming training?",
    "I want to start boxing, what do I need?",
    "Is there anything for football players?",  # no está en el catálogo
]

for query in queries:
    print(f"\nPregunta: {query}")
    response = rag_chain.invoke(query)
    print(f"Respuesta: {response}")