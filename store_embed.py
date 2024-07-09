# from qdrant_client import QdrantClient
# from qdrant_client.http.models import Distance, VectorParams, PointStruct, VectorStruct
# from embed import get_embeddings
# import json 
# client = QdrantClient(":memory:")
# def store_embeddings(embeddings, processed_resumes):
   

#     collection_name = "resume"
#     vector_name = "default"

#     # Check if the collection exists, if not create it
#     if not client.collection_exists(collection_name):
#         vector_params = VectorParams(size=384, distance=Distance.COSINE)
#         client.create_collection(
#             collection_name=collection_name,
#             vectors_config=vector_params
#         )

#     # Prepare points to be inserted into the collection
#     points = []
#     for i, embedding in enumerate(embeddings):
#         points.append(PointStruct(
#             id=i,
#             vector=embedding.tolist(),
#             payload=processed_resumes[i]
#         ))

    
#     client.upsert(collection_name=collection_name, points=points)

#     print("Embeddings stored successfully.")

# with open('processed_resumes.json', 'r') as f:
#     processed_resumes = json.load(f)

# texts = [resume['text'] for resume in processed_resumes]
# embeddings = get_embeddings(texts)
# store_embeddings(embeddings, processed_resumes)
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams,VectorStruct, PointStruct, MultiVectorConfig,MultiVectorComparator
from embed import get_embeddings
from dotenv import load_dotenv
load_dotenv()
import os
import json
import logging

client = QdrantClient(url="https://cd543e04-34c7-4592-b68e-e0c6932f7d40.us-east4-0.gcp.cloud.qdrant.io",api_key=os.environ["api_key"])  # Use an in-memory database for testing

def store_embeddings(embeddings, processed_resumes):
    collection_name = "resume"
    vector_name = "default"  # Ensure this matches the vector name used in Qdrant

    logging.info(f"Storing embeddings for {len(embeddings)} resumes.")

    # Check if the collection exists, if not create it
    if not client.collection_exists(collection_name):
        vector_params ={"text": VectorParams(size=384, distance=Distance.COSINE,multivector_config=MultiVectorConfig(
            comparator=MultiVectorComparator.MAX_SIM
        ),)}
        logging.info(f"Creating collection '{collection_name}' with vector params: {vector_params}")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=vector_params
        )

    # # Check if the collection exists, if not create it
    # if not client.collection_exists(collection_name):
    #     vector_params = VectorParams(size=384, distance=Distance.COSINE)
    #     client.
    #     client.create_collection(
    #         collection_name=collection_name,
    #         vectors_config=vector_params
    #     )

    # Prepare points to be inserted into the collection
    points = []
    for i, embedding in enumerate(embeddings):
        points.append(PointStruct(
            id=i,
            vector={"text":embedding.tolist()},
            payload={"resume":processed_resumes[i]}
        ))
        

    client.upsert(collection_name=collection_name, points=points, wait=True)
    print("Embeddings stored successfully.")


with open('processed_resumes.json', 'r') as f:
    processed_resumes = json.load(f)
texts = [resume['text'] for resume in processed_resumes]
embeddings = get_embeddings(texts)
store_embeddings(embeddings, processed_resumes)