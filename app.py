from flask import Flask, request, jsonify, make_response, send_from_directory
from flask_cors import CORS
from hashlib import md5
import os

cors = CORS(supports_credentials=True)

app = Flask(__name__)
cors.init_app(app)
upload_dir = 'upload'


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    data = file.read()
    ext = os.path.splitext(file.filename)[-1]
    url = md5(data).hexdigest() + ext
    with open(upload_dir + '/' + url, 'wb') as f:
        f.write(data)
    return jsonify({
        'code': 200,
        'url': '/uploads/' + url
    })


@app.route('/uploads/<filename>', methods=['GET'])
def get_file(filename):
    return make_response(send_from_directory(upload_dir, filename))


if __name__ == '__main__':
    os.makedirs(upload_dir, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
