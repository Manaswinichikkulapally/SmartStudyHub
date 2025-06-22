import fitz  # PyMuPDF
import nltk
import re

# ✅ Smart way to avoid downloading every time
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Extract text from uploaded PDF
def extract_text_from_pdf(file_path):
    text = ''
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    return text

# Clean and summarize text
def clean_text(text):
    return re.sub(r'\s+', ' ', text)

def summarize_text(text):
    sentences = nltk.sent_tokenize(text)
    return ' '.join(sentences[:2])  # first 2 sentences

# Predict tag based on keywords
def predict_tag(text):
    keywords = {
        'SQL': ['query', 'sql', 'table', 'database'],
        'GATE': ['syllabus', 'marks', 'gate', 'subjects'],
        'Python': ['python', 'code', 'function', 'loop'],
        'Java': ['java', 'class', 'object', 'inheritance'],
        'AI': ['agent', 'intelligence', 'environment'],
    }
    text = text.lower()
    for tag, words in keywords.items():
        if any(word in text for word in words):
            return tag
    return "General"

# Main processor function
def process_pdf(file_path):
    text = extract_text_from_pdf(file_path)
    text = clean_text(text)
    summary = summarize_text(text)
    tag = predict_tag(text)
    summary += "\n\n© 2025 Chikkulapally Manaswini - SmartStudyHub"
    return summary, tag
