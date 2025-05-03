
from flask import Blueprint, request, jsonify, session
from services.use_case_handler import UseCaseHandler
from services.user_services import user_service
import traceback
import json
from utils.logger import *

image_routes = Blueprint("image_routes", __name__)

@image_routes.route("/create", methods=["POST"])
def create_image():
    """Unified endpoint for all image generation use cases"""
    try:
        # Get JSON data or form data
        if request.is_json:
            data = request.json
            prompt = data.get("prompt")
            use_case = data.get("use_case", "text_to_image")
            engine = data.get("engine", "stability_ai")
            options = data.get("options", {})

            # No image file in JSON requests
            image = None
        else:
            # Form data
            prompt = request.form.get("prompt")
            use_case = request.form.get("use_case", "text_to_image")
            engine = request.form.get("engine", "stability_ai")
            options_str = request.form.get("options", "{}")
            
            # Try to parse options as JSON
            try:
                options = json.loads(options_str)
            except:
                options = {}
            
            # Check for image file
            image = None
            if 'image' in request.files:
                image = request.files['image'].stream
        
        # Validate required parameters
        if not prompt:
            return jsonify({"status": "error", "message": "Prompt is required"}), 400
        
        # Process the request using the use case handler
        image_path, prompt_id = UseCaseHandler.handle_use_case(
            use_case=use_case,
            engine_name=engine,
            prompt=prompt,
            image=image,
            options=options
        )
        
        eval_logger.info("Image gen Completed")

        return jsonify({
            "status": "success", 
            "image": image_path,
            "prompt_id": prompt_id,
            "details": {
                "use_case": use_case,
                "engine": engine
            }
        })

    except ValueError as e:
        # Handle validation errors
        return jsonify({"status": "error", "message": str(e)}), 400

    except Exception as e:
        # Handle other errors
        error_details = traceback.format_exc()
        print(f"Error processing request: {error_details}")
        return jsonify({
            "status": "error", 
            "message": f"An error occurred: {str(e)}"
        }), 500

# User-specific routes

@image_routes.route("/history", methods=["GET"])
def get_user_history():
    """Get current user's prompt history"""
    try:
        history = user_service.get_prompt_history()
        return jsonify({
            "status": "success",
            "history": history
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500

@image_routes.route("/shortlist", methods=["POST"])
def shortlist_image():
    """Shortlist an image for the current user"""
    try:
        data = request.json
        image_path = data.get("image_path")
        prompt_id = data.get("prompt_id")
        
        if not image_path or not prompt_id:
            return jsonify({
                "status": "error",
                "message": "Image path and prompt ID are required"
            }), 400
        
        shortlisted = user_service.shortlist_image(image_path, prompt_id)
        
        return jsonify({
            "status": "success",
            "message": "Image shortlisted successfully",
            "shortlisted": shortlisted
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500

@image_routes.route("/shortlisted", methods=["GET"])
def get_shortlisted():
    """Get all shortlisted images for the current user"""
    try:
        shortlisted = user_service.get_shortlisted_images()
        return jsonify({
            "status": "success",
            "shortlisted": shortlisted
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500

@image_routes.route("/feedback", methods=["POST"])
def submit_feedback():
    """Submit feedback for a generated image/prompt"""
    try:
        data = request.json
        prompt_id = data.get("prompt_id")
        rating = data.get("rating")
        comments = data.get("comments")
        
        if not prompt_id or rating is None:
            return jsonify({
                "status": "error",
                "message": "Prompt ID and rating are required"
            }), 400
        
        # Validate rating (1-5)
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({
                "status": "error",
                "message": "Rating must be an integer between 1 and 5"
            }), 400
        
        feedback = user_service.save_feedback(prompt_id, rating, comments)
        
        return jsonify({
            "status": "success",
            "message": "Feedback submitted successfully",
            "feedback": feedback
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500

# For backward compatibility, keep the original endpoints with updated implementations

@image_routes.route("/text-to-image", methods=["POST"])
def text_to_image():
    """Legacy endpoint for text-to-image generation"""
    if request.is_json:
        prompt = request.json.get("prompt")
        engine = request.json.get("engine", "stability_ai")
        options = request.json.get("options", {})
    else:
        prompt = request.form.get("prompt")
        engine = request.form.get("engine", "stability_ai")
        options_str = request.form.get("options", "{}")

        try:
            options = json.loads(options_str)
        except:
            options = {}

    try:
        image_path, prompt_id = UseCaseHandler.handle_use_case(
            use_case="text_to_image",
            engine_name=engine,
            prompt=prompt,
            options=options
        )
        eval_logger.info("Text to Image Completed")
        return jsonify({
            "status": "success", 
            "image": image_path,
            "prompt_id": prompt_id
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@image_routes.route("/sketch-to-image", methods=["POST"])
def sketch_to_image():
    """Legacy endpoint for sketch-to-image generation"""
    prompt = request.form.get("prompt")
    engine = request.form.get("engine", "stability_ai")
    options_str = request.form.get("options", "{}")

    try:
        options = json.loads(options_str)
    except:
        options = {}

    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "No sketch file provided"}), 400

    sketch = request.files['image'].stream

    try:
        image_path, prompt_id = UseCaseHandler.handle_use_case(
            use_case="sketch_to_image",
            engine_name=engine,
            prompt=prompt,
            image=sketch,
            options=options
        )

        eval_logger.info("Sketch to Image Completed")
        
        return jsonify({
            "status": "success", 
            "image": image_path,
            "prompt_id": prompt_id
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500