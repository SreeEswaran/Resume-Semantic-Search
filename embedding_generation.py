from sentence_transformers import SentenceTransformer
import numpy as np

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Read the parsed resumes
with open('../parsed_resumes.txt', 'r') as f:
    resume_texts = f.read().split('='*80 + '\n')

# Generate embeddings
resume_embeddings = model.encode(resume_texts, convert_to_tensor=True)

# Save embeddings and texts
np.save('../resume_embeddings.npy', resume_embeddings.detach().cpu().numpy())
with open('../resume_texts.txt', 'w') as f:
    for text in resume_texts:
        f.write(text + '\n' + '='*80 + '\n')
