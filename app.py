from flask import Flask, render_template, request, send_file
import os
import PyPDF2
import zipfile

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
ZIP_FOLDER = "zip_output"

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(ZIP_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER
app.config["ZIP_FOLDER"] = ZIP_FOLDER


def split_pdf(input_pdf, output_folder, pages_per_file):
    """Splits a PDF into multiple files with the specified number of pages per file."""
    with open(input_pdf, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)
        filenames = []

        for start_page in range(0, total_pages, pages_per_file):
            writer = PyPDF2.PdfWriter()
            end_page = min(start_page + pages_per_file, total_pages)

            for page_num in range(start_page, end_page):
                writer.add_page(reader.pages[page_num])

            output_filename = os.path.join(output_folder, f"pages_{start_page + 1}_to_{end_page}.pdf")
            with open(output_filename, "wb") as output_file:
                writer.write(output_file)

            filenames.append(output_filename)

    return filenames


def create_zip_file(output_files, zip_folder, zip_filename="split_pdfs.zip"):
    """Compresses all split PDFs into a ZIP file."""
    zip_filepath = os.path.join(zip_folder, zip_filename)

    with zipfile.ZipFile(zip_filepath, "w") as zipf:
        for file in output_files:
            zipf.write(file, os.path.basename(file))  # Add file to ZIP

    return zip_filepath


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files or "pages_per_file" not in request.form:
            return "No file uploaded or no page count provided", 400

        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400

        try:
            pages_per_file = int(request.form["pages_per_file"])
            if pages_per_file <= 0:
                return "Invalid number of pages per file", 400
        except ValueError:
            return "Invalid input for pages per file", 400

        # Save uploaded file
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        # Split PDF
        split_filenames = split_pdf(filepath, app.config["OUTPUT_FOLDER"], pages_per_file)

        # Create ZIP of all output PDFs
        zip_filepath = create_zip_file(split_filenames, app.config["ZIP_FOLDER"])

        return render_template("index.html", filenames=[os.path.basename(f) for f in split_filenames], zip_filename=os.path.basename(zip_filepath))

    return render_template("index.html")


@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(app.config["OUTPUT_FOLDER"], filename), as_attachment=True)


@app.route("/download_zip/<zip_filename>")
def download_zip(zip_filename):
    return send_file(os.path.join(app.config["ZIP_FOLDER"], zip_filename), as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
