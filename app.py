from flask import Flask, jsonify, session
from routes.image_routes import image_routes
from routes.tech_pack_and_size_chart import tech_pack_routes
from routes.project_routes import project_routes
import os
import secrets

app = Flask(__name__)

# Set up session with a secret key
app.secret_key = secrets.token_hex(16)  # Generate a random secret key
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions on disk
app.config['SESSION_PERMANENT'] = True  # Make sessions persistent
app.config['PERMANENT_SESSION_LIFETIME'] = 86400 * 30  # 30 days session lifetime

# Register Blueprints
app.register_blueprint(image_routes, url_prefix='/generate')
app.register_blueprint(tech_pack_routes, url_prefix='/generate')
app.register_blueprint(project_routes, url_prefix='/api')

# Create outputs directory if it doesn't exist
os.makedirs("outputs", exist_ok=True)

# Basic health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Service is running"})

# User status endpoint
@app.route('/user/status', methods=['GET'])
def user_status():
    user_id = session.get('user_id', 'Not logged in')
    return jsonify({
        "status": "success",
        "user_id": user_id,
        "is_logged_in": user_id != 'Not logged in'
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)