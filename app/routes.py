from flask import Blueprint

# Create a blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route("/")
def home():
    return "<h1>Welcome to Migration Portal API</h1>", 200
