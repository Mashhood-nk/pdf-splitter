from flask import Flask, render_template, request, send_file
import os
import PyPDF2

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER


def split_pdf(input_pdf, output_folder):
    with open(input_pdf, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        filenames = []
        for page_num in range(len(reader.pages)):
            writer = PyPDF2.PdfWriter()
            writer.add_page(reader.pages[page_num])
            output_filename = os.path.join(output_folder, f"page_{page_num + 1}.pdf")
            with open(output_filename, "wb") as output_file:
                writer.write(output_file)
            filenames.append(f"page_{page_num + 1}.pdf")
    return filenames


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded", 400
        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400

        # Save uploaded file
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        # Split PDF
        filenames = split_pdf(filepath, app.config["OUTPUT_FOLDER"])

        return render_template("index.html", filenames=filenames)

    return render_template("index.html")


@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(app.config["OUTPUT_FOLDER"], filename), as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
