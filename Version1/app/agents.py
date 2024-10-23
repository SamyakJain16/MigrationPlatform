"""
This handles user management, such as adding users, viewing user lists, and updating user information.
"""

from flask import Blueprint, request, jsonify
from .supabase import supabase_client
from flask_jwt_extended import jwt_required, get_jwt_identity


agents_bp = Blueprint('agents', __name__)


@agents_bp.route("/agents", methods=["GET"])
def list_agents():
    try:
        users = supabase_client.table('users').select("*").execute()
        return jsonify(users.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# app/users.py (Flask backend)


agents_bp = Blueprint('agents', __name__)


users_bp = Blueprint('users', __name__)


@agents_bp.route("/add_client", methods=["POST"])
@jwt_required()  # Ensure the request has a valid JWT token
def add_client():
    try:
        # Log the received data
        data = request.get_json()
        name = data.get("name")
        client_email = data.get("email")
        status = data.get("status", "Pending")

        # Get the agent's ID (identity) from the JWT token
        agent_id = get_jwt_identity()  # Now contains the agent's UUID from the JWT
        print(f"Agent ID from Backend-JWT(add_client): {agent_id}")

        # Insert the client into the clients table
        result = supabase_client.table('clients').insert({
            "agent_id": agent_id,   # Directly use the agent's UUID
            "name": name,
            "email": client_email,
            "status": status
        }).execute()

        print(f"Insert result: {result}")
        if not result.data:
            return jsonify({"error": "Failed to add client"}), 400

        return jsonify({"message": "Client added successfully", "client_id": result.data[0]['id']}), 201

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


@agents_bp.route("/clients", methods=["GET"])
@jwt_required()  # Ensure JWT is required
def list_clients():
    try:
        # Get the agent's UUID from the JWT token
        agent_id = get_jwt_identity()
        print("Agent ID from Backend-JWT(list_clients):", agent_id)

        # Fetch all clients for the logged-in agent using the agent's UUID
        clients = supabase_client.table('clients').select(
            "*").eq("agent_id", agent_id).execute()
        print("Clients Backend", clients)

        return jsonify(clients.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@agents_bp.route("/update_client", methods=["PUT"])
def update_client():
    data = request.get_json()
    client_id = data.get("client_id")
    updated_info = {}

    if "name" in data:
        updated_info["name"] = data["name"]
    if "email" in data:
        updated_info["email"] = data["email"]
    if "status" in data:
        updated_info["status"] = data["status"]

    try:
        # Update client details in the clients table
        result = supabase_client.table('clients').update(
            updated_info).eq("id", client_id).execute()
        return jsonify({"message": "Client updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@agents_bp.route("/delete_client", methods=["DELETE"])
def delete_client():
    client_id = request.args.get("client_id")

    try:
        # Delete client from the clients table
        result = supabase_client.table(
            'clients').delete().eq("id", client_id).execute()
        return jsonify({"message": "Client deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
