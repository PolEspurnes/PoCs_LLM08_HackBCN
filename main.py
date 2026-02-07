from embeddings import *
from llm_utils import ask_llm


if __name__ == "__main__":
	load_embeddings()
	query=input("Question: ")
	datos_denuncia = similarity_search(query)
	respuesta = ask_llm(datos_denuncia)
	print(respuesta)
