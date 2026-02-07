from sentence_transformers import SentenceTransformer
import faiss
from pathlib import Path
import json


embed_model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.IndexFlatL2(embed_model.get_sentence_embedding_dimension())


denuncias = []
denuncias_metadata = []


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


def similarity_search(query):
	if not denuncias:
		return []

	q_emb = embed_model.encode([query]).astype("float32")
	D, I = index.search(q_emb, k=1)

	denuncia = denuncias[I[0][0]]
	metadata = denuncias_metadata[I[0][0]]
	
	retrieved = denuncia + json.dumps(metadata)
	print(retrieved)

	return retrieved
