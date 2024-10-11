from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
import uuid
from .supabase import supabase_client

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Generate a unique agent ID
        agent_id = str(uuid.uuid4())

        # Data to insert
        agent_data = {
            "id": agent_id,          # Use the generated UUID
            "email": email,          # Agent's email
            "password": hashed_password  # Hashed password
        }

        # Insert the data into the 'agents' table
        result = supabase_client.table('agents').insert(agent_data).execute()

        # Check if the result has data
        if result.data:
            return jsonify({"message": "Agent registered successfully", "agent_id": agent_id}), 201
        else:
            return jsonify({"error": "Failed to register agent"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    try:
        # Fetch the agent from the database using email
        agent = supabase_client.table('agents').select(
            "*").eq("email", email).execute()
        if not agent.data:
            return jsonify({"error": "Invalid email or password"}), 401

        # Check if the password matches
        if check_password_hash(agent.data[0]['password'], password):
            # Create a JWT access token using agent ID instead of email
            agent_id = agent.data[0]['id']
            access_token = create_access_token(identity=agent_id)
            return jsonify({"access_token": access_token}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_agent = get_jwt_identity()  # Retrieve the agent's UUID from JWT
    return jsonify(logged_in_as=current_agent), 200


"""
This handles all the authentication routes (login, signup, logout). You can use Supabase's authentication feature to manage users.




from flask import Blueprint, request, jsonify
from .supabase import supabase_client

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    try:
        # Register the user in Supabase's auth system
        response = supabase_client.auth.sign_up(
            {"email": email, "password": password})
        agent_id = response.user.id  # UUID from Supabase
        print(agent_id)
        # Optionally, store agent details in the agents table
        # Add the agent to your custom agents table
        supabase_client.table('agents').insert({
            "id": agent_id,
            "email": email,
            "name": None  # You can capture more info later
        }).execute()

        return jsonify({"message": "User registered successfully", "agent_id": agent_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    try:
        # Login user via Supabase
        response = supabase_client.auth.sign_in_with_password(
            {"email": email, "password": password})
        token = response.session.access_token  # Get the session token
        return jsonify({"token": token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401
"""
