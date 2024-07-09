import os
import requests
import pdfplumber

def download_resume(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)

def parse_resume(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

if __name__ == "__main__":
    resume_urls = ['link1', 'link2', 'link3']  # Add your resume URLs here
    resume_texts = []
    os.makedirs('../resumes', exist_ok=True)
    for i, url in enumerate(resume_urls):
        save_path = f'../resumes/resume_{i}.pdf'
        download_resume(url, save_path)
        resume_texts.append(parse_resume(save_path))

    with open('../parsed_resumes.txt', 'w') as f:
        for text in resume_texts:
            f.write(text + '\n' + '='*80 + '\n')
