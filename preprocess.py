import os
import json
from PyPDF2 import PdfReader

def preprocess_resumes(resume_folder):
    processed_resumes = []
    for filename in os.listdir(resume_folder):
        if filename.endswith('.pdf'):
            resume_path = os.path.join(resume_folder, filename)
            text = extract_text_from_pdf(resume_path)
            resume_data = {
                'filename': filename,
                'text': text
            }
            processed_resumes.append(resume_data)
    return processed_resumes

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(open(pdf_path, 'rb'))
    except:
         return ""
    text = ''
    for page_num in range(len(reader.pages)):
        try:
            text += reader.pages[page_num].extract_text()
        except:
            pass
        
    
    return text

def save_processed_resumes(processed_resumes, output_path):
    with open(output_path, 'w') as f:
        json.dump(processed_resumes, f)

processed_resumes = preprocess_resumes('resume_dataset')
save_processed_resumes(processed_resumes, 'processed_resumes.json')