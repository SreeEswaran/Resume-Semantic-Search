echo "preprocessing the resumes"
python3 preprocess.py
echo "preprocessing done"
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org fastembed
echo "generating embeddings and bieng stored"
python3 embed.py
echo "embeddings generated"

echo "starting the server"
python3 main.py