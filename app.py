# app.py
from flask import Flask, jsonify
from routes.image_routes import image_routes
from routes.tech_pack_and_size_chart import tech_pack_routes
import os


app = Flask(__name__)

# Register Blueprints
app.register_blueprint(image_routes, url_prefix='/generate')
app.register_blueprint(tech_pack_routes, url_prefix='/generate')

# Create outputs directory if it doesn't exist
os.makedirs("outputs", exist_ok=True)

# Basic health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Service is running"})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)