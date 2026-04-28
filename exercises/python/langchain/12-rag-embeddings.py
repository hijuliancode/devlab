# Objetivo: entender qué es un embedding antes de construir el RAG completo.
# Un embedding convierte texto en un array de números que captura su significado.

from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# El modelo de embedding es diferente al modelo de generación de texto.
# Este modelo convierte texto en números, no genera respuestas.
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")

# Convertimos tres frases en embeddings
frases = [
  "My dog loves to play in the park", # sobre un perro
  "My cat sleeps all day on the couch", # sobre un gato, similar a la anterior
  "The stock market crashed yesterday" # sobre finanzas muy diferente
]

vectors = embeddings_model.embed_documents(frases)

# Cada frase se convierte en un array de números
print(f"Número de frases: {len(vectors)}")
print(f"Dimensiones de cada embedding: {len(vectors[0])}")
print(f"\nPrimeros 5 números del embedding de la frase 1: {vectors[0][:5]}")
print(f"\nPrimeros 5 números del embedding de la frase 2: {vectors[1][:5]}")
print(f"\nPrimeros 5 números del embedding de la frase 3: {vectors[2][:5]}")


# Ahora calculamos similitud coseno manualmente para ver qué tan parecidas son.
# La similitud coseno va de -1 (opuestos) a 1 (idénticos).
# Frases con significados similares deberían tener valores más cercanos a 1.
import numpy as np

def cosine_similarity(vec1, vec2):
  vec1 = np.array(vec1)
  vec2 = np.array(vec2)
  return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

sim_1_2 = cosine_similarity(vectors[0], vectors[1])
sim_1_3 = cosine_similarity(vectors[0], vectors[2])

print(f"\nSimilitud entre frase 1 (perro) y frase 2 (gato): {sim_1_2:.4f}")
print(f"Similitud entre frase 1 (perro) y frase 3 (finanzas): {sim_1_3:.4f}")
print("\nLa similitud entre perro y gato debería ser mayor que entre perro y finanzas.")
print("Eso demuestra que los embeddings capturan significado, no solo palabras.")
