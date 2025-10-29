import os
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from model import predict_authenticity

# Initialize the Flask application
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Allowed file types for upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to check for allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    """Renders the main page with the file upload form."""
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify_certificate():
    """Handles the certificate upload and verification process."""
    if 'certificate' not in request.files:
        return jsonify({'error': 'No file part in the request.'}), 400
    
    file = request.files['certificate']

    if file.filename == '':
        return jsonify({'error': 'No file selected.'}), 400

    if file and allowed_file(file.filename):
        # Secure the filename to prevent directory traversal attacks
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Call the machine learning model to get the prediction
            # This function is defined in model.py
            result = predict_authenticity(filepath)
            
            # Clean up the uploaded file after processing
            os.remove(filepath)

            return jsonify(result)

        except Exception as e:
            # Clean up the file in case of an error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'An error occurred during processing: {str(e)}'}), 500

    else:
        return jsonify({'error': 'File type not allowed.'}), 400

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)