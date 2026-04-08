from sentence_transformers import SentenceTransformer
from dotenv import dotenv_values
import numpy as np
import faiss

try:
    index = faiss.read_index("faiss_index.bin")
except:
    index = "Testing"
    print("Fais index not found")

OPEN_ROUTER_KEY = dotenv_values(".env")["OPEN_ROUTER_KEY"]



football_concepts = [
    "fútbol",
    "partido de fútbol",
    "jugador de fútbol",
    "gol",
    "liga de fútbol",
    "champions league",
    "mundial de fútbol",
    "árbitro de fútbol",
    "reglas del fútbol",
    "LaLiga",
    "Estadisticas fútbol",
    "Historia del fútbol",
    "Reglamento de fútbol",
]



use_model = SentenceTransformer("all-MiniLM-L6-v2")

football_embeddings = use_model.encode(football_concepts).astype("float32")

forbidden_terms = ["Javier Tebas"]
forbidden_embeddings = use_model.encode(forbidden_terms).astype("float32")

def forbidden_filter(query, threshold=0.80):
    q_emb = use_model.encode([query]).astype("float32")

    # normalizar
    q_norm = q_emb / np.linalg.norm(q_emb, axis=1, keepdims=True)
    f_norm = forbidden_embeddings / np.linalg.norm(forbidden_embeddings, axis=1, keepdims=True)

    similarities = np.dot(q_norm, f_norm.T)[0]
    best_score = similarities.max()

    print(f"[Similitud término prohibido: {best_score:.3f}]")

    return best_score >= threshold  # True = bloquear
    
def football_domain_filter(query, threshold=0.55):
    # q_emb = use_model.encode([query]).astype("float32")

    # q_norm = q_emb / np.linalg.norm(q_emb, axis=1, keepdims=True)
    # f_norm = football_embeddings / np.linalg.norm(football_embeddings, axis=1, keepdims=True)

    # similarities = np.dot(q_norm, f_norm.T)[0]
    # best_score = similarities.max()

    # print(f"[Dominio fútbol: {best_score:.3f}]")

    # return best_score >= threshold
    q_emb = use_model.encode([query]).astype("float32")

    # Normalizar (igual que FAISS si usaste cosine)
    faiss.normalize_L2(q_emb)

    # Buscar en el índice
    distances, indices = index.search(q_emb, k)

    best_score = distances[0][0]

    print(f"[FAISS dominio fútbol score: {best_score:.3f}]")

    return best_score >= threshold