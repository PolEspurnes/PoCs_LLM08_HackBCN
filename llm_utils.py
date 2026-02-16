import requests
import json
from dotenv import dotenv_values

OPEN_ROUTER_KEY = dotenv_values(".env")["OPEN_ROUTER_KEY"]
MODEL = dotenv_values(".env")["MODEL"]

PROMPT_1 = """
Eres un asistente virtual de backoffice que debe ayudar con la gestión de denuncias enviadas relacionadas con
establecimientos que consumen contenido pirata. 
Tu funcionalidad es la de resumir y dar opinión sobre las denuncias, dando criterio a las observaciones adjuntadas por los denunciantes. 
Debes responder en base al 'Relevant context' que te será proporcionado, que será la información de la denuncia.
El formato de tu respuesta debe ser solamente text. No uses markdown ni HTML.
"""

PROMPT_2 = """
Eres un asistente virtual que permite devolver información de estadisticas de fútbol, permitiendo a los fans de los distintos equipos
de LaLIGA obtener datos de sus equipos, jugadores, información relevante e incluso reglas y noticias de fútbol.
"""


def request_openrouter(payload):
	r = requests.post(
		"https://openrouter.ai/api/v1/chat/completions",
		headers={
			"Authorization": "Bearer "+OPEN_ROUTER_KEY,
			"Content-Type": "application/json",
		},
		data=json.dumps(payload)
	)

	if r.status_code != 200:
		print("HTTP ERROR:", r.status_code, r.text)
		return "Error en la conexión con el modelo."

	data = r.json()

	if "choices" not in data or not data["choices"]:
		print("ERROR API:", data)
		return "El modelo no pudo responder (error de API)."


	return data["choices"][0]["message"]["content"]


def ask_llm(retrieved_text):
	payload = {
		"model": MODEL,   # Openrouter model
		"max_tokens": 500,
		"messages": [
			{"role": "system", "content": PROMPT_1},
			{"role": "user", "content": f"Relevant context:\n{retrieved_text}"}
		]
	}

	return request_openrouter(payload)
	

def ask_llmSemantic(query):
	payload = {
		"model": MODEL,
		"max_tokens": 2000,
		"messages": [
			{"role": "system","content": PROMPT_2},
			{"role": "user","content": f"Contexto:\n\n\nPregunta: {query}"}
		]
	}

	return request_openrouter(payload)