from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from search_engine import SemanticSearchEngine
from data_loader import load_resumes

class QueryModel(BaseModel):
    query: str
    top_k: int = 10

# Load initial resumes (if any)
urls = ["https://example.com/resume1.pdf", "https://example.com/resume2.pdf"]
resumes = load_resumes(urls)

search_engine = SemanticSearchEngine()
if resumes:
    search_engine.build_index(resumes)

app = FastAPI()

@app.post("/upload_resumes/")
async def upload_resumes(files: list[UploadFile] = File(...)):
    global search_engine
    new_resumes = load_resumes(files=files)
    resumes.extend(new_resumes)
    search_engine.build_index(resumes)
    return {"message": "Resumes uploaded and indexed successfully"}

@app.post("/search/")
def search_resumes(query: QueryModel):
    results = search_engine.search(query.query, query.top_k)
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
