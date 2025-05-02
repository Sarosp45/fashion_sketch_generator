# routes/tech_pack_and_size_chart.py
from flask import Blueprint, request, jsonify
import json
import requests
import traceback
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEYS = os.getenv("OPENAI_API_KEY")



tech_pack_routes = Blueprint("tech_pack_routes", __name__)

def generate_with_openai(prompt, model="gpt-4-turbo"):
    """Generate content using OpenAI's GPT models"""
    if "openai" not in API_KEYS:
        return {"error": "OpenAI API key not configured"}
    
    api_key = API_KEYS["openai"]
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    url = "https://api.openai.com/v1/chat/completions"
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a fashion and apparel expert."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if not response.ok:
            return {"error": f"OpenAI API error: {response.text}"}
        
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        return {"content": content}
    
    except Exception as e:
        return {"error": f"Error generating content: {str(e)}"}

@tech_pack_routes.route("/tech-pack", methods=["POST"])
def generate_tech_pack():
    """Generate a technical pack for apparel"""
    try:
        # Get data from request
        if request.is_json:
            data = request.json
            product_type = data.get("product_type", "")
            details = data.get("details", "")
            engine = data.get("engine", "openai")
        else:
            product_type = request.form.get("product_type", "")
            details = request.form.get("details", "")
            engine = request.form.get("engine", "openai")
        
        # Validate input
        if not product_type:
            return jsonify({"status": "error", "message": "Product type is required"}), 400
        
        # Create prompt for tech pack
        prompt = f"""
        Create a detailed technical pack for a {product_type}.
        
        Additional details: {details}
        
        Include the following sections:
        1. Product specifications
        2. Materials and components
        3. Construction details
        4. Measurements
        5. Production guidelines
        6. Quality control points
        
        Format the response in a structured way with clear headings.
        """
        
        # Currently only support OpenAI for tech packs
        if engine != "openai":
            return jsonify({
                "status": "warning", 
                "message": f"Engine {engine} not supported for tech packs, using OpenAI instead.",
                "tech_pack": generate_with_openai(prompt)
            })
        
        result = generate_with_openai(prompt)
        
        if "error" in result:
            return jsonify({"status": "error", "message": result["error"]}), 500
        
        return jsonify({
            "status": "success", 
            "tech_pack": result["content"]
        })
    
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Error generating tech pack: {error_details}")
        return jsonify({
            "status": "error", 
            "message": f"An error occurred: {str(e)}"
        }), 500

@tech_pack_routes.route("/size-chart", methods=["POST"])
def generate_size_chart():
    """Generate a size chart for apparel"""
    try:
        # Get data from request
        if request.is_json:
            data = request.json
            product_type = data.get("product_type", "")
            region = data.get("region", "International")
            gender = data.get("gender", "Unisex")
            engine = data.get("engine", "openai")
        else:
            product_type = request.form.get("product_type", "")
            region = request.form.get("region", "International")
            gender = request.form.get("gender", "Unisex")
            engine = request.form.get("engine", "openai")
        
        # Validate input
        if not product_type:
            return jsonify({"status": "error", "message": "Product type is required"}), 400
        
        # Create prompt for size chart
        prompt = f"""
        Create a detailed size chart for {gender} {product_type} using {region} sizing standards.
        
        Format the response as a structured table with:
        1. Size designations (S, M, L or numerical sizes)
        2. Key measurements in both inches and centimeters
        3. Include appropriate fitting guidelines
        
        The response should be well-formatted and ready to use in product documentation.
        """
        
        # Currently only support OpenAI for size charts
        if engine != "openai":
            return jsonify({
                "status": "warning", 
                "message": f"Engine {engine} not supported for size charts, using OpenAI instead.",
                "size_chart": generate_with_openai(prompt)
            })
        
        result = generate_with_openai(prompt)
        
        if "error" in result:
            return jsonify({"status": "error", "message": result["error"]}), 500
        
        return jsonify({
            "status": "success", 
            "size_chart": result["content"]
        })
    
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Error generating size chart: {error_details}")
        return jsonify({
            "status": "error", 
            "message": f"An error occurred: {str(e)}"
        }), 500