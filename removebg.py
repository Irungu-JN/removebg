#pip install flask rembg pillow werkzeug
#pip install onnxruntime


import os
from flask import Flask, request, render_template, send_from_directory
from rembg import remove
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Directory to store uploaded and processed images
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER

# Allowed image extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]
        if file.filename == "":
            return "No selected file"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            output_path = os.path.join(app.config["PROCESSED_FOLDER"], f"no_bg_{filename}")

            # Save original image
            file.save(input_path)

            # Remove background
            image = Image.open(input_path)
            output_image = remove(image)
            output_image.save(output_path)

            return f"""
            <h3>Background removed!</h3>
            <p>Original Image:</p>
            <img src="/uploads/{filename}" width="300">
            <p>Processed Image:</p>
            <img src="/processed/no_bg_{filename}" width="300">
            <br><br>
            <a href="/processed/no_bg_{filename}" download>Download Processed Image</a>
            """

    return '''
    <h2>Upload an Image</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".jpg,.jpeg,.png">
        <input type="submit" value="Upload">
    </form>
    '''

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/processed/<filename>")
def processed_file(filename):
    return send_from_directory(app.config["PROCESSED_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)
