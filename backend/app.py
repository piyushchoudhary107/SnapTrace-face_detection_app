from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from face_detector import detect_faces

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static', exist_ok=True)

@app.route('/')
def home():
    return "Flask server is running. use /upload via post to send an image"

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image found'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    result_path, face_count = detect_faces(path)

    return jsonify({
    "face_count": face_count,
    "faces": [f"/static/face_{i}.jpg" for i in range(face_count)]
})


if __name__ == '__main__':
    app.run(debug=True)
