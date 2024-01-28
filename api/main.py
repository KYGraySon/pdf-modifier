import os
import time
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS, cross_origin
from replace import replaceTexts
from text import replaceText

app = Flask(__name__)
origin = "http://localhost:5173"
CORS(app, resources={r"/api/*": {"origins": origin}})

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER


@app.route("/", methods={"POST"})
@cross_origin(origin=origin, headers=["Content-Type", "Authorization"])
def home():
    try:
        # Check if the 'file' key is in the request.files dictionary
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files["file"]
        # Check if the file has a name
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        target_text = "{{Full name}}"
        replacement_text = "Adam"
        filePath = replaceText(file_path, target_text, replacement_text)
        filename = "downloaded_file.pdf"
        time.sleep(1)
        return send_file(filePath, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/add-input", methods={"POST"})
@cross_origin(origin=origin, headers=["Content-Type", "Authorization"])
def addInput():
    try:
        # Check if the 'file' key is in the request.files dictionary
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files["file"]
        # Check if the file has a name
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        target_texts = [["[[Signature_1]]"], ["[[Signature_2]]"], ["[[Signature_3]]"]]
        filePath = replaceTexts(file_path, target_texts)
        filename = "downloaded_file.pdf"
        time.sleep(1)
        return send_file(filePath, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
