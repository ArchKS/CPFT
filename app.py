from flask import Flask, request, send_from_directory, flash, redirect, url_for, render_template,jsonify
from pathlib import Path
import socket
import json
import os

UPLOAD_FOLDER = './uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    return send_from_directory('.', 'index.html')

@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(directory=Path(app.config['UPLOAD_FOLDER']), path=filename)


@app.route('/list_files', methods=['GET'])
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return json.dumps(files)



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return jsonify(success=False, error='No file part in the request'), 400

    files = request.files.getlist('files')
    errors = []

    for file in files:
        if file.filename == '':
            errors.append('No selected file')
            continue

        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            errors.append(f'File "{file.filename}" has an invalid extension')

    if errors:
        return jsonify(success=False, error=', '.join(errors)), 400
    else:
        return jsonify(success=True)


@app.route('/delete', methods=['POST'])
def delete_files():
    files = os.listdir(UPLOAD_FOLDER)
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
    return jsonify({'result': 'All files deleted.'})




def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip



if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host='0.0.0.0', port=5100)
