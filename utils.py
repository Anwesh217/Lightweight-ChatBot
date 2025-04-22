import fitz  # PyMuPDF
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Split text into reasonable chunks
def chunk_text(text, chunk_size=500):
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# Extract text from PDF file
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)
    return text

# Find top N most relevant chunks using TF-IDF
def get_relevant_chunks(query, chunks, top_k=4):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    vectorizer = TfidfVectorizer().fit_transform([query] + chunks)
    similarities = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()
    ranked_indices = similarities.argsort()[-top_k:][::-1]
    return [chunks[i] for i in ranked_indices]
