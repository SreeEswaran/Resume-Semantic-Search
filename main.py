from fastapi import FastAPI, Query
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Initialize FastAPI
app = FastAPI()

# Load the model and embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
resume_embeddings = np.load('../resume_embeddings.npy')
with open('../parsed_resumes.txt', 'r') as f:
    resume_texts = f.read().split('='*80 + '\n')

# Create FAISS index
embedding_dim = resume_embeddings.shape[1]
index = faiss.IndexFlatL2(embedding_dim)
index.add(resume_embeddings)

@app.get("/search")
def search(query: str, top_k: int = 10):
    query_embedding = model.encode([query], convert_to_tensor=True).detach().cpu().numpy()
    distances, indices = index.search(query_embedding, top_k)
    results = [resume_texts[idx] for idx in indices[0]]
    return {"results": results}

# To run the server: uvicorn app.main:app --reload
