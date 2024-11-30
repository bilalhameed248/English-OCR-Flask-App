from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
import os

app = Flask(__name__)
app.secret_key="Secret Key"
CORS(app)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method =='POST':
        if 'file' in request.files:
            file = request.files['file']
            if file:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(image_path)
                extracted_text = perform_ocr(image_path)
                print("\n\nextracted_text:",extracted_text,"\n\n")
                data = {'extracted_text': extracted_text}
                response =  jsonify(data)
                response.headers.add('Access-Control-Allow-Origin', '*')
                response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
                response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
                response.headers.add('Access-Control-Allow-Credentials', 'true')
                return response
        # If no valid file is provided or an error occurs
        return jsonify({'error': 'Invalid request or file processing error'})
    else:
        return render_template('index.html')


def perform_ocr(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
