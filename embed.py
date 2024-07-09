from transformers import AutoTokenizer, AutoModel

import torch
model_name="sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def get_embeddings(texts):
    
    embeddings = []
    for text in texts:
        inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        outputs = model(**inputs)
        embeddings.append(outputs.last_hidden_state.mean(dim=1).detach().numpy())
    return embeddings

def get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    return model(**inputs).last_hidden_state.mean(dim=1).detach().numpy()


# from transformers import AutoTokenizer, AutoModel
# import torch

# model_name = "sentence-transformers/all-MiniLM-L6-v2"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModel.from_pretrained(model_name)

# def get_embeddings(texts):
#     embeddings = []
#     for text in texts:
#         inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
#         with torch.no_grad():
#             outputs = model(**inputs)
#         embeddings.append(outputs.last_hidden_state.mean(dim=1).detach().numpy())
#     return embeddings

# from qdrant_client import QdrantClient

# client = QdrantClient(":memory:")  # Use an in-memory database for testing

# def store_embeddings(embeddings, processed_resumes):
#     client.recreate_collection(collection_name="resumes", vector_size=384, distance="Cosine")

#     points = []
#     for i, embedding in enumerate(embeddings):
#         points.append({
#             'id': i,
#             'vector': embedding.tolist(),
#             'payload': processed_resumes[i]
#         })
#     client.upsert(collection_name="resumes", points=points)

# with open('processed_resumes.json', 'r') as f:
#     processed_resumes = json.load(f)

# texts = [resume['text'] for resume in processed_resumes]
# embeddings = get_embeddings(texts)
# store_embeddings(embeddings, processed_resumes)
