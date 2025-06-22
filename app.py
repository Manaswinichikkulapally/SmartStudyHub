"""
SmartStudyHub - AI Powered Study Resource App

Copyright (c) 2025 Chikkulapally Manaswini
Unauthorized copying, distribution, or reuse of this code is strictly prohibited.
This software is intended only for academic demonstration.

GitHub: https://github.com/YourUsername/SmartStudyHub
"""

print("⚠️  Copyright Notice")
print("📚 Project: SmartStudyHub")
print("👩‍💻 Developer: Chikkulapally Manaswini")
print("🚫 Unauthorized use or plagiarism is not allowed.\n")

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
from nlp_model import process_pdf

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    file_data = []
    for file in files:
        filepath = os.path.join(UPLOAD_FOLDER, file)
        summary, tag = process_pdf(filepath)
        file_data.append({'filename': file, 'tag': tag, 'summary': summary})
    return render_template('index.html', files=file_data)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        pdf = request.files['pdf']
        if pdf:
            filename = secure_filename(pdf.filename)
            pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ✅ Correct PORT for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


