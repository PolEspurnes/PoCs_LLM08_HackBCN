import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

print("Cargando modelo de embeddings...")
model = SentenceTransformer("all-MiniLM-L6-v2")



# ----------- FUNCIÓN CHUNKING -------------
def chunk_text(text, chunk_size=400, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

# ----------- LEER Y DIVIDIR DOCUMENTOS -------------
documents = []

print("Leyendo documentos y creando chunks...")
for file in os.listdir("docs"):
    with open(f"docs/{file}", "r", encoding="utf-8") as f:
        text = f.read()
        chunks = chunk_text(text)
        documents.extend(chunks)

print(f"Total chunks creados: {len(documents)}")

# ----------- CREAR EMBEDDINGS -------------
print("Creando embeddings...")
doc_embeddings = model.encode(documents).astype("float32")
faiss.normalize_L2(doc_embeddings)

# ----------- CREAR ÍNDICE FAISS -------------
dim = doc_embeddings.shape[1]
index = faiss.IndexFlatIP(dim)
index.add(doc_embeddings)

# ----------- GUARDAR -------------
print("Guardando índice...")
faiss.write_index(index, "faiss_index.bin")
np.save("documents.npy", documents)

print("✅ Índice FAISS con chunking creado correctamente")