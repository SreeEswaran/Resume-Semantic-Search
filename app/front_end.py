import streamlit as st
from search_engine import SemanticSearchEngine
from data_loader import load_resumes

# Streamlit app
st.title("Resume Semantic Search")

uploaded_files = st.file_uploader("Upload Resumes", accept_multiple_files=True, type=['pdf'])
urls = st.text_area("Enter URLs of resumes (one per line)").splitlines()
resumes = load_resumes(urls, uploaded_files)

if resumes:
    search_engine = SemanticSearchEngine()
    search_engine.build_index(resumes)
    
    query = st.text_input("Enter your query:")
    if query:
        results = search_engine.search(query)
        for resume in results:
            st.write(resume)
