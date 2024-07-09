from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

class SemanticSearchEngine:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.resumes = []

    def build_index(self, resumes):
        self.resumes = resumes
        embeddings = self.model.encode(resumes)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings))

    def search(self, query, top_k=10):
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding), k=top_k)
        return [self.resumes[i] for i in indices[0]]

# Example usage
if __name__ == "__main__":
    from data_loader import load_resumes
    
    urls = ["https://example.com/resume1.pdf", "https://example.com/resume2.pdf"]
    resumes = load_resumes(urls)
    
    search_engine = SemanticSearchEngine()
    search_engine.build_index(resumes)
    
    query = "Python developer with experience scaling AWS infrastructure"
    results = search_engine.search(query)
    print(results)
