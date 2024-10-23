from flask import Blueprint, request, jsonify
from .supabase import supabase_client

# Define the Blueprint for document management
documents_bp = Blueprint('documents', __name__)

# Example route for uploading documents (replace with actual functionality)


@documents_bp.route("/upload", methods=["POST"])
def upload_document():
    file = request.files['file']
    user_id = request.form['user_id']

    try:
        # Implement the logic for document upload here
        # For example: Upload the file to Supabase storage
        file_path = f"documents/{user_id}/{file.filename}"
        supabase_client.storage.from_(
            "documents").upload(file_path, file.stream)
        return jsonify({"message": "Document uploaded successfully", "file_path": file_path}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
