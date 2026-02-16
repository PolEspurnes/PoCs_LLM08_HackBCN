import requests
import json
from dotenv import dotenv_values

OPEN_ROUTER_KEY = dotenv_values(".env")["OPEN_ROUTER_KEY"]
MODEL = dotenv_values(".env")["MODEL"]

PROMPT = """
Eres un asistente virtual de backoffice que debe ayudar con la gestión de denuncias enviadas relacionadas con
establecimientos que consumen contenido pirata. 
Tu funcionalidad es la de resumir y dar opinión sobre las denuncias, dando criterio a las observaciones adjuntadas por los denunciantes. 
Debes responder en base al 'Relevant context' que te será proporcionado, que será la información de la denuncia.
"""


def ask_llm(retrieved_text):
	payload = {
		"model": MODEL,   # Openrouter model
		"max_tokens": 500,
		"messages": [
			{"role": "system", "content": PROMPT},
			{"role": "user", "content": f"Relevant context:\n{retrieved_text}"}
		]
	}

	r = requests.post(
		"https://openrouter.ai/api/v1/chat/completions",
		headers={
			"Authorization": "Bearer "+OPEN_ROUTER_KEY,
			"Content-Type": "application/json",
		},
		data=json.dumps(payload)
	).json()

	return r["choices"][0]["message"]["content"]
    
