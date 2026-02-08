import json
import random
import os
import string


def generate_filename():
	allowed = string.ascii_uppercase + string.digits
	return ''.join(random.choice(allowed) for _ in range(5))+".json"


def nueva_denuncia(data):
	filename = generate_filename()
	with open("./denuncias/"+filename, "w", encoding="utf-8") as f:
		json.dump(data, f, ensure_ascii=False, indent=2)