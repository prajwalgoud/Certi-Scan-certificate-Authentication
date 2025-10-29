# CertiScan: Smart Certificate Authentication 📜✨

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-black?logo=flask)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn)
![OCR](https://img.shields.io/badge/OCR-Tesseract-blueviolet)

> A web application built with Python and Flask that uses machine learning and OCR to intelligently verify the authenticity of uploaded certificates. This project is designed to save time and prevent fraud for HR professionals, recruiters, and academic reviewers.

---

## 📸 Screenshots

( **Action for you:** Create a folder named `screenshots` in your project, and add your app screenshots to it.)

| Main Upload Page | "Authentic" Result | "Potentially Forged" Result |
| :---: | :---: | :---: |
| ![Main Page](screenshots/main-page.png) | ![Authentic Result](screenshots/authentic-result.png) | ![Forged Result](screenshots/forged-result.png) |

---

## ✨ Core Features

* **Multi-Format Support:** Verifies `.pdf`, `.png`, and `.jpg` certificate files.
* **OCR Integration:** Uses **PyTesseract** (for images) and **PyMuPDF** (for PDFs) to extract text from any document.
* **ML-Powered Verification:** Analyzes document features (keywords, dates, issuer names) using a rule-based model that simulates a Scikit-learn classifier.
* **Trusted Database:** Validates the extracted issuer name against a **SQLite** database of trusted institutions.
* **Instant Feedback:** Provides an immediate prediction ("Authentic" or "Potentially Forged") with a confidence score.
* **Secure & Private:** Uploaded files are deleted from the server immediately after processing.

---

## 🛠️ Tech Stack

* **Backend:** **Python**, **Flask** (for the web server and API)
* **Machine Learning:** **Scikit-learn** (simulated via a rule-based scoring engine)
* **Text Extraction:** **PyTesseract** (Tesseract-OCR), **PyMuPDF (fitz)**
* **Database:** **SQLite**
* **Frontend:** HTML, CSS, JavaScript (Fetch API)

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project running on your local machine.

### Prerequisites

You must have the following software installed on your system:

1.  **Git:** [Download Git](https://git-scm.com/downloads)
2.  **Python 3.8+:** [Download Python](https://www.python.org/downloads/)
3.  **Tesseract-OCR:** This is a **critical** dependency.
    * **Windows:** Download and run the installer from [here](https://github.com/UB-Mannheim/tesseract/wiki).
    * **macOS:** `brew install tesseract`
    * **Linux:** `sudo apt-get install tesseract-ocr`

    **IMPORTANT:** After installing Tesseract, you **must** update the `tesseract_cmd` path in `model.py` to match its location on your system (e.g., `r'C:\Program Files\Tesseract-OCR\tesseract.exe'`).

### Installation & Execution

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourUsername/CertiScan-Project.git](https://github.com/YourUsername/CertiScan-Project.git)
    cd CertiScan-Project
    ```
    *(Replace `YourUsername/CertiScan-Project.git` with your actual repository URL)*

2.  **Create and activate a virtual environment:**
    ```bash
    # Create the environment
    python -m venv venv

    # Activate it (Windows)
    .\venv\Scripts\activate
    
    # Activate it (macOS/Linux)
    # source venv/bin/activate
    ```

3.  **Install the required libraries:**
    (First, create the `requirements.txt` file from Step 2 below, then run:)
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create and populate the database:**
    This script will create `certiscan.db` and load issuers from your JSON file.
    ```bash
    python create_db.py
    ```

5.  **Run the application:**
    ```bash
    python app.py
    ```

6.  **Open in your browser:**
    Navigate to **`http://127.0.0.1:5000`**

---

## 📁 Project Structure
