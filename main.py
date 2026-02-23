from flask import Flask, request, jsonify
from parser import JitterbitJSONParser
import tempfile
import os

app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "Jitterbit Parser API Running"}

@app.route("/parse", methods=["POST"])
def parse_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if not file.filename.endswith(".json"):
        return jsonify({"error": "Only .json project files supported"}), 400

    # Save temp file (handles large 50-100MB safely)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        file.save(tmp.name)
        temp_path = tmp.name

    try:
        parser = JitterbitJSONParser(temp_path)
        result = parser.parse()
        return jsonify(result)

    finally:
        os.remove(temp_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
