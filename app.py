import os
from flask import Flask, request, render_template, send_file
from PIL import Image
import imagehash
from hash_functions import final  # Importing the final function from hash_functions.py

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file part"
    file = request.files["file"]
    if file.filename == "":
        return "No selected file"
    if file:
        # Save uploaded image
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        # Call the final function from hash_functions.py to compute hashes
        original_hash, embedded_hash = final(file_path)

        download_link = None
        if embedded_hash:
            download_link = "/download"

        return render_template(
            "index.html",
            original_hash=original_hash,
            embedded_hash=embedded_hash,
            download_link=download_link,
        )


@app.route("/download")
def download():
    return send_file("uploads/embedded_image.jpeg", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
