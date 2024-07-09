import requests
from io import BytesIO
import fitz  # PyMuPDF
import os

def fetch_resume(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    return None

def parse_pdf(file):
    document = fitz.open(stream=file, filetype='pdf')
    text = ""
    for page in document:
        text += page.get_text()
    return text

def load_resumes(urls=None, files=None):
    resumes = []
    if urls:
        for url in urls:
            file = fetch_resume(url)
            if file:
                text = parse_pdf(file)
                resumes.append(text)
    if files:
        for file in files:
            if file:
                text = parse_pdf(file)
                resumes.append(text)
    return resumes
