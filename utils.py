import json
import random
import os
import string
import re


def generate_filename():
	allowed = string.ascii_uppercase + string.digits
	return ''.join(random.choice(allowed) for _ in range(5))+".json"


def nueva_denuncia(data):
	filename = generate_filename()
	with open("./denuncias/"+filename, "w", encoding="utf-8") as f:
		json.dump(data, f, ensure_ascii=False, indent=2)

def normalize_query(query: str) -> str:
    # Reemplazos case-insensitive
    query = re.sub(r"\bXavier\b", "Javier", query, flags=re.IGNORECASE)
    query = re.sub(r"\bLollevas\b", "Tebas", query, flags=re.IGNORECASE)
    query = re.sub(r"\bElCampeonato\b", "LaLiga", query, flags=re.IGNORECASE)
    query = re.sub(r"\bEl Campeonato\b", "La Liga", query, flags=re.IGNORECASE)
    return query

def denormalize_output(text: str) -> str:
    text = re.sub(r"\bJavier\b", "Xavier", text, flags=re.IGNORECASE)
    text = re.sub(r"\bTebas\b", "Lollevas", text, flags=re.IGNORECASE)
    text = re.sub(r"\bLaLiga\b", "ElCampeonato", text, flags=re.IGNORECASE)
    return text