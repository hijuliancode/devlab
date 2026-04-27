# Memoria en LLMs y LangChain

## Por qué existe este concepto

Los LLMs son stateless por diseño. Cada llamada a la API es completamente 
independiente, el modelo no recuerda nada de lo anterior. Cuando un chatbot 
"recuerda" la conversación, no es una capacidad del modelo sino código externo 
que reenvía el historial completo en cada llamada.

LangChain automatiza ese manejo con diferentes estrategias. Los conceptos 
aplican sin importar la versión de LangChain o si usamos LangGraph.

---

## Las 5 estrategias de memoria

**1. Sin memoria**
Cada mensaje se envía solo, sin historial. El modelo responde únicamente al 
mensaje actual sin ningún contexto previo. Es el comportamiento por defecto 
al llamar directamente a la API.

**2. Buffer completo (ConversationBufferMemory)**
Se envía toda la conversación completa en cada llamada: todos los mensajes del 
usuario y todas las respuestas del modelo, desde el inicio. Es la estrategia 
más simple pero la más costosa en tokens para conversaciones largas.

**3. Ventana de mensajes (ConversationBufferWindowMemory)**
Se envían solo los últimos k intercambios. Lo anterior se descarta. El modelo 
literalmente olvida lo que quedó fuera de la ventana. Útil para conversaciones 
donde solo importa el contexto reciente.

**4. Límite de tokens (ConversationTokenBufferMemory)**
Similar a la ventana pero el límite se define en tokens en vez de en número de 
mensajes. Es más preciso porque un intercambio puede ser corto o muy largo, y 
los proveedores cobran por tokens, no por mensajes.

**5. Resumen automático (ConversationSummaryBufferMemory)**
Los intercambios recientes se guardan completos hasta cierto límite de tokens. 
Lo que excede ese límite no se descarta sino que se comprime: el modelo genera 
un resumen de la conversación antigua y ese resumen viaja como contexto. Es la 
estrategia más inteligente para conversaciones largas donde el contexto 
histórico importa.

---

## Por qué no hay ejercicios de estas estrategias aquí

Las clases `ConversationBufferMemory` y sus variantes fueron deprecadas en 
LangChain y estaban programadas para eliminarse en v1.0.0. El reemplazo 
moderno usa LangGraph con checkpointers (`MemorySaver`, `SqliteSaver`, 
`PostgresSaver`), que es una librería separada con su propio modelo mental.

Los ejercicios prácticos de memoria quedan pendientes para cuando estudie 
LangGraph de forma dedicada. Los conceptos de las 5 estrategias siguen siendo 
válidos, solo cambia la API para implementarlos.

---

## Lo que no cambia

El concepto central es siempre el mismo: construir y enviar una lista de 
mensajes al modelo. LangChain, LangGraph, o cualquier framework futuro son 
distintas formas de automatizar ese patrón. Entender el patrón es valioso