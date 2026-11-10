
from flask import Flask, request, jsonify, render_template_string
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Sunglasses AI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            background: #101010;
            color: white;
            font-family: Arial;
            text-align: center;
            padding: 40px 15px;
        }
        h1 { color: #00d5ff; }
        .card {
            background: #202020;
            padding: 25px;
            border-radius: 15px;
            max-width: 400px;
            margin: 30px auto;
        }
        input, button {
            padding: 12px;
            margin: 12px;
            border-radius: 8px;
        }
        button {
            background: #00d5ff;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>🕶️ Sunglasses AI</h1>
    <p>Your Virtual Sunglasses Experience</p>

    <div class="card">
        <h2>Upload Your Photo</h2>
        <form action="/upload" method="POST"
              enctype="multipart/form-data">
            <input type="file" name="photo"
                   accept="image/*" required>
            <br>
            <button type="submit">Upload Photo</button>
        </form>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/upload", methods=["POST"])
def upload():
    if "photo" not in request.files:
        return jsonify({"error": "No photo selected"}), 400

    photo = request.files["photo"]

    if not photo.filename:
        return jsonify({"error": "Select a photo"}), 400

    filename = secure_filename(photo.filename)

    if "." not in filename:
        return jsonify({"error": "Invalid file"}), 400

    extension = filename.rsplit(".", 1)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        return jsonify({"error": "Image format not supported"}), 400

    return jsonify({
        "message": "Photo uploaded successfully!",
        "filename": filename,
        "next_step": "AI sunglasses processing"
    })


@app.route("/health")
def health():
    return jsonify({"status": "Sunglasses AI is running"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
