"""
This is where you would create routes to display client insights and analytics.


"""

from flask import Blueprint, jsonify
from .supabase import supabase_client

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route("/dashboard", methods=["GET"])
def get_dashboard_data():
    try:
        pending_clients = supabase_client.table('users').select(
            "*").eq("status", "Pending").execute()
        approved_clients = supabase_client.table('users').select(
            "*").eq("status", "Approved").execute()

        dashboard_data = {
            "pending_clients": len(pending_clients.data),
            "approved_clients": len(approved_clients.data)
        }

        return jsonify(dashboard_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
