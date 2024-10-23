"""
This handles status updates for the migration process (e.g., pending, approved, rejected).


"""

from flask import Blueprint, request, jsonify
from .supabase import supabase_client

status_bp = Blueprint('status', __name__)


@status_bp.route("/update_status", methods=["POST"])
def update_status():
    data = request.get_json()
    user_id = data.get("user_id")
    status = data.get("status")

    try:
        supabase_client.table('users').update(
            {"status": status}).eq("id", user_id).execute()
        return jsonify({"message": "Status updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
