import os
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import PyPDF2

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf_file' not in request.files:
        return "No file part"

    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return "No selected file"

    if pdf_file:
        pdf_filename = secure_filename(pdf_file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
        pdf_file.save(pdf_path)
        return "File uploaded successfully"

@app.route('/get_answer', methods=['POST'])
def get_answer():
    question = request.form['question']
    pdf_filename = request.form['pdf_filename']
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)

    # Read the PDF and extract text
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        text = ""
        for page_num in range(pdf_reader.numPages):
            text += pdf_reader.getPage(page_num).extractText()

    # Here you can use a language model (e.g., GPT-3) to generate an answer based on the question and the extracted text.
    # Replace the following line with your actual code.
    answer = "This is a sample answer."

    return answer

# Correct line to serve static files
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
