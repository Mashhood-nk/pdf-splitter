# PDF Splitter Web App

A simple Flask-based web application to split PDFs into individual pages. Upload a PDF, and the app will generate separate files for each page, allowing you to download them individually.

## 🚀 Features
- Upload a PDF file and split it into separate pages
- Download each page as an individual PDF file
- Web-based interface built using Flask


## 🔧 Installation

   1. **Clone the repository:**
      ```sh
      git clone https://github.com/mashhood-nk/pdf-splitter.git
      cd pdf-splitter
      ```
   2. **Create a virtual environment (optional but recommended):**
      ```sh
      python -m venv venv
      source venv/bin/activate  # On Windows use: venv\Scripts\activate
      ```
   3. **Install dependencies:**
      ```sh
      pip install -r requirements.txt
      ```
   
   5. **Run the application:**
      ```sh
      python app.py
      ```
   
   6. **Open in your browser:**
      ```
      http://127.0.0.1:5000
      ```
   
   ## 📁 Project Structure
   ```
   📂 pdf-splitter/
   ├── 📄 app.py            # Main Flask application
   ├── 📂 templates/
   │   ├── index.html      # Frontend UI
   ├── 📂 uploads/         # Folder for uploaded PDFs
   ├── 📂 output/          # Folder for split PDF pages
   ├── 📄 requirements.txt # Dependencies
   ├── 📄 README.md        # Project documentation
   ```

   ## 🌐 Deployment
   You can deploy this app on:
   - **Render** ([render.com](https://render.com))
   - **Hugging Face Spaces** ([huggingface.co/spaces](https://huggingface.co/spaces))

   For deployment, use **Gunicorn**:
   ```sh
   pip install gunicorn
   ```
   And run:
   ```sh
   gunicorn -w 4 app:app
   ```

   ## 📜 License
   This project is licensed under the MIT License.

   ## 📬 Contact
   For any questions or suggestions, reach out via [your email] or [your LinkedIn].
   ```

3. **Save the file and add it to your GitHub repository.**

