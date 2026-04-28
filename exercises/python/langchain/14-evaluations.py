# Evaluation en LangChain
#
# Esta clase la dejo pendiente para profundizar más adelante.
# El concepto central es: ¿cómo sé si mi app con LLMs está respondiendo bien?
#
# El problema es que no puedo comparar strings exactos como en tests normales.
# "Sí tiene bolsillos" y "Efectivamente cuenta con bolsillos laterales" son
# la misma respuesta pero como strings son completamente diferentes.
#
# Las 4 estrategias que cubre el curso:
#
# 1. Ejemplos manuales: creo pares de pregunta/respuesta esperada a mano.
#    Simple pero no escala.
#
# 2. Ejemplos generados por LLM: le doy mis documentos al modelo y le pido
#    que genere preguntas y respuestas de prueba automáticamente.
#
# 3. Debug con langchain.debug = True: no es evaluación sino inspección.
#    Imprime todo lo que pasa internamente: qué documentos recuperó el
#    retriever, qué prompt llegó al modelo, cuántos tokens usó.
#    Útil para entender por qué algo falla.
#
# 4. Evaluación asistida por LLM: uso otro LLM para comparar la respuesta
#    real con la esperada y decidir si son semánticamente equivalentes.
#    Es la estrategia más poderosa y la más usada en producción hoy.
#
# La idea que me parece más interesante: usar un LLM para evaluar otro LLM
# no es circular. El modelo evaluador solo necesita ser bueno comparando
# significados, no saber el contenido. Es como contratar a alguien para
# revisar el trabajo de otro.
#
# Estado actual (2026):
# QAEvalChain y QAGenerateChain están deprecados desde v0.1.0.
# El reemplazo moderno es LangSmith, la plataforma oficial de LangChain
# para evaluación en producción. Tiene UI, persistencia, experimentos
# comparativos y trazabilidad completa de cada llamada al modelo.
#
# Pendiente: estudiar LangSmith cuando profundice en LangChain.
# Documentación: https://docs.smith.langchain.com
