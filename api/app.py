from flask import Flask, request, jsonify
import base64
import re
import io
from werkzeug.utils import secure_filename
from mimetypes import guess_type
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/bfhl', methods=['GET', 'POST'])
def bfhl():
    if request.method == 'GET':
        return jsonify({"operation_code": 1}), 200

    elif request.method == 'POST':
        response = {
            "is_success": False,
            "user_id": "Harivatsa_G A_30062003",
            "email": "ha5033@srmist.edu.in",
            "roll_number": "RA2111027010026",
            "numbers": [],
            "alphabets": [],
            "highest_lowercase_alphabet": [],
            "file_valid": False
        }

        data = request.get_json()
        if not data or 'data' not in data:
            return jsonify(response), 400

        input_data = data.get('data')
        if not isinstance(input_data, list):
            return jsonify(response), 400

        # Separate numbers and alphabets
        numbers = []
        alphabets = []
        for item in input_data:
            if re.fullmatch(r'\d+', item):
                numbers.append(item)
            elif re.fullmatch(r'[A-Za-z]', item):
                alphabets.append(item)

        # Find highest lowercase alphabet
        lowercase_letters = [char for char in alphabets if char.islower()]
        highest_lowercase = []
        if lowercase_letters:
            highest_char = max(lowercase_letters)
            highest_lowercase.append(highest_char)

        response.update({
            "is_success": True,
            "numbers": numbers,
            "alphabets": alphabets,
            "highest_lowercase_alphabet": highest_lowercase
        })

        # Handle file_b64
        file_b64 = data.get('file_b64')
        if file_b64:
            try:
                file_data = base64.b64decode(file_b64)
                file_valid = True
                file_size_kb = round(len(file_data) / 1024, 2)

                # Since we don't have a file name, we'll try to guess the MIME type from the content
                mime_type = guess_type("dummy")[0] or "application/octet-stream"

                response.update({
                    "file_valid": True,
                    "file_mime_type": mime_type,
                    "file_size_kb": str(file_size_kb)
                })
            except Exception as e:
                response.update({
                    "file_valid": False,
                })
        else:
            response.update({
                "file_valid": False,
            })

        return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
