from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from pathlib import Path



embed_model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.IndexFlatL2(embed_model.get_sentence_embedding_dimension())


denuncias = []

def load_embeddings():

	for p in Path('./denuncias/').glob('*.json'):
		denuncias.append(p.read_text())

	embeddings_denuncias = embed_model.encode(denuncias).astype("float32")

	# Build FAISS index
	index.add(embeddings_denuncias)


def similarity_search(query):
	if not denuncias:
		return []

	q_emb = embed_model.encode([query]).astype("float32")
	D, I = index.search(q_emb, k=1)

	retrieved = denuncias[I[0][0]]

	return retrieved