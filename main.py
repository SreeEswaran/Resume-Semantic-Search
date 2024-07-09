from fastapi import FastAPI, Query
from embed import get_embedding
from store_embed import client
import numpy as np
app = FastAPI()


@app.get("/search")
def search(query: str = Query(...)):
    embedding = get_embedding(query)
    search_result = client.search(
        collection_name="resume",
        query_vector=("text",embedding.tolist()),
        limit=10  # Use 'limit' instead of 'top'
    )
    return search_result
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=3000)
