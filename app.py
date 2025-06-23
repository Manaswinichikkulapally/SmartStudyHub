from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
from nlp_model import process_pdf

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

if __name__ == '__main__':
    app.run(debug=True)
