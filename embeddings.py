from sentence_transformers import SentenceTransformer
import faiss
from pathlib import Path
import json
import numpy as np


embed_model = SentenceTransformer("all-MiniLM-L6-v2")
dimension = embed_model.get_sentence_embedding_dimension()


# PoC 1
index = faiss.IndexFlatL2(dimension)
denuncias = []
denuncias_metadata = []


# PoC 3
## Usaremos IP (inner product) -> buscar por similitud coseno (mejor en busquedas semanticas)
index_poc3 = faiss.IndexFlatIP(dimension)
faqs_data = []


def load_embeddings():

	for p in Path('./denuncias/').glob('*.json'):
		data = json.loads(p.read_text())

		metadata = {
			"nombre_bar": data.get("nombre_bar"),
			"fecha_denuncia": data.get("fecha_denuncia"),
		}
		
		denuncias_metadata.append(metadata)
		
		embedding_text = f"Bar ubicado en {data.get('poblacion')} denunciado por {data.get('observaciones')}"

		denuncias.append(embedding_text)

	embeddings_denuncias = embed_model.encode(denuncias).astype("float32")

	# Build FAISS index
	index.add(embeddings_denuncias)


def load_embeddings_poc3():
	
	questions = []

	for p in Path('./docs_poc3/').glob('*.json'):
		data = json.loads(p.read_text())
		
		for q in data:
			faqs_data.append(q)
			questions.append(q["question"])

	

	# Normalizamos los embeddings
	embeddings = embed_model.encode(questions, normalize_embeddings=True)

	# Build FAISS index
	index_poc3.add(np.array(embeddings).astype("float32"))


def similarity_search(query):
	if not denuncias:
		return []

	q_emb = embed_model.encode([query]).astype("float32")
	D, I = index.search(q_emb, k=1)

	denuncia = denuncias[I[0][0]]
	metadata = denuncias_metadata[I[0][0]]
	
	retrieved = denuncia + json.dumps(metadata)
	#print(retrieved)

	return retrieved


def similarity_search_poc3(query, k=2, threshold=0.65):
	if not faqs_data:
		return []

	# Embedding de la pregunta del usuario
	q_emb = embed_model.encode([query], normalize_embeddings=True)

	scores, indices = index_poc3.search(np.array(q_emb).astype("float32"), k)

	results = []

	for score, idx in zip(scores[0], indices[0]):
		if score >= threshold:
			results.append(faqs_data[idx]["answer"])
			#print(score)
			#print(faqs_data[idx]["answer"])

	return results