import requests
import json
from dotenv import dotenv_values

config = dotenv_values(".env")
OPEN_ROUTER_KEY = config["OPEN_ROUTER_KEY"]
MODEL = config["MODEL"]

PROMPT = """
Eres un asistente virtual que permite devolver información de estadisticas de fútbol, permitiendo a los fans de los distintos equipos
de LaLIGA obtener datos de sus equipos, jugadores, información relevante e incluso reglas y noticias de fútbol.
"""
    
def ask_llmSemantic(query):
    payload = {
        "model": MODEL,
        "max_tokens": 2000,
        "messages": [
            {
                "role": "system",
                "content": PROMPT
            },
            {
                "role": "user",
                "content": f"Contexto:\n\n\nPregunta: {query}"
            }
        ]
    }

    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer "+OPEN_ROUTER_KEY,
            "Content-Type": "application/json",
        },
       #data=json.dumps(payload)
       json=payload
    )
    
    print("STATUS CODE:", r.status_code)
    print("RAW RESPONSE:", r.text)
    
    if r.status_code != 200:
        print("HTTP ERROR:", r.status_code, r.text)
        return "Error en la conexión con el modelo."
    
    data = r.json()
    
    if "choices" not in data or not data["choices"]:
        print("ERROR API:", data)
        return "El modelo no pudo responder (error de API)."
        
    

    return data["choices"][0]["message"]["content"]