import pytesseract
from PIL import Image
import re
import json
import fitz  # PyMuPDF for handling PDF files


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load the trusted issuer database
with open('trusted_issuers.json', 'r') as f:
    ISSUER_DATABASE = json.load(f)['trusted']

# --- Helper Functions ---

def extract_text_from_image(image_path):
    """Extracts text from an image file using Tesseract OCR."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text.lower()
    except Exception as e:
        print(f"Error processing image: {e}")
        return ""

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file using PyMuPDF."""
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        return text.lower()
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ""

def preprocess_and_extract_features(text):
    """
    Analyzes the extracted text to create features for the model.
    """
    features = {
        'issuer_found': None,
        'has_certificate_keyword': False,
        'has_signature_keyword': False,
        'has_date': False
    }

    # 1. Check for trusted issuer
    for issuer in ISSUER_DATABASE:
        if issuer in text:
            features['issuer_found'] = issuer
            break
    
    # 2. Check for common certificate keywords
    certificate_keywords = ['certificate', 'award', 'completion', 'degree', 'diploma']
    if any(keyword in text for keyword in certificate_keywords):
        features['has_certificate_keyword'] = True

    # 3. Check for keywords indicating a signature
    signature_keywords = ['signature', 'signed', 'director', 'hod', 'head of department']
    if any(keyword in text for keyword in signature_keywords):
        features['has_signature_keyword'] = True
        
    # 4. Check for a date (simple regex for YYYY-MM-DD or DD-MM-YYYY)
    if re.search(r'\d{2,4}[-/]\d{2}[-/]\d{2,4}', text):
        features['has_date'] = True
        
    return features

def evaluate_features(features):
    """
    Simulates a trained ML model using a rule-based scoring system.
    """
    score = 0
    total_possible_score = 100
    
    # Define scoring rules
    if features['issuer_found']:
        score += 50
    if features['has_certificate_keyword']:
        score += 20
    if features['has_signature_keyword']:
        score += 20
    if features['has_date']:
        score += 10

    confidence = (score / total_possible_score)
    
    # Determine prediction based on a threshold
    is_authentic = score > 60
    
    prediction = "Authentic" if is_authentic else "Potentially Forged"
    
    details = f"Issuer check: {'Found (' + str(features['issuer_found']) + ')' if features['issuer_found'] else 'Not Found'}. "
    details += f"Keywords valid: {features['has_certificate_keyword']}. "
    details += f"Signature hint: {features['has_signature_keyword']}. "
    details += f"Date found: {features['has_date']}."
    
    return {
        'prediction': prediction,
        'confidence_score': f"{confidence:.2f}",
        'details': details
    }

def predict_authenticity(file_path):
    """
    Main function to orchestrate the certificate verification process.
    """
    file_extension = file_path.rsplit('.', 1)[1].lower()
    
    # Step 1: Extract text
    if file_extension in ['png', 'jpg', 'jpeg']:
        extracted_text = extract_text_from_image(file_path)
    elif file_extension == 'pdf':
        extracted_text = extract_text_from_pdf(file_path)
    else:
        raise ValueError("Unsupported file type")

    if not extracted_text:
        return {'error': 'Could not extract any text from the document.'}

    # Step 2: Extract features
    features = preprocess_and_extract_features(extracted_text)
    
    # Step 3: Get prediction
    result = evaluate_features(features)
    
    return result