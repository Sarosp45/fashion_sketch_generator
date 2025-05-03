from flask import Blueprint, request, jsonify
from services.project_services import project_service
import traceback

project_routes = Blueprint("project_routes", __name__)

@project_routes.route("/projects", methods=["POST"])
def create_project():
    """Create a new project"""
    try:
        data = request.json
        name = data.get("name")
        description = data.get("description")
        
        if not name:
            return jsonify({
                "status": "error",
                "message": "Project name is required"
            }), 400
        
        project = project_service.create_project(name, description)
        
        return jsonify({
            "status": "success",
            "project": project
        })
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Error creating project: {error_details}")
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500

@project_routes.route("/projects", methods=["GET"])
def get_user_projects():
    """Get all projects for the current user"""
    try:
        projects = project_service.get_user_projects()
        
        return jsonify({
            "status": "success",
            "projects": projects
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500

@project_routes.route("/projects/<project_id>", methods=["GET"])
def get_project(project_id):
    """Get a project by ID"""
    try:
        project = project_service.get_project(project_id)
        
        if not project:
            return jsonify({
                "status": "error",
                "message": "Project not found"
            }), 404
        
        return jsonify({
            "status": "success",
            "project": project
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500

@project_routes.route("/projects/<project_id>", methods=["PUT"])
def update_project(project_id):
    """Update a project"""
    try:
        data = request.json
        name = data.get("name")
        description = data.get("description")
        metadata = data.get("metadata")
        
        project = project_service.update_project(
            project_id=project_id,
            name=name,
            description=description,
            metadata=metadata
        )
        
        if not project:
            return jsonify({
                "status": "error",
                "message": "Project not found or you don't have permission to update it"
            }), 404
        
        return jsonify({
            "status": "success",
            "project": project
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500

@project_routes.route("/projects/<project_id>", methods=["DELETE"])
def delete_project(project_id):
    """Delete a project"""
    try:
        success = project_service.delete_project(project_id)
        
        if not success:
            return jsonify({
                "status": "error",
                "message": "Project not found or you don't have permission to delete it"
            }), 404
        
        return jsonify({
            "status": "success",
            "message": "Project deleted successfully"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500

@project_routes.route("/projects/<project_id>/prompts", methods=["POST"])
def add_prompt_to_project(project_id):
    """Add a prompt to a project"""
    try:
        data = request.json
        prompt_id = data.get("prompt_id")
        
        if not prompt_id:
            return jsonify({
                "status": "error",
                "message": "Prompt ID is required"
            }), 400
        
        project = project_service.add_prompt_to_project(project_id, prompt_id)
        
        if not project:
            return jsonify({
                "status": "error",
                "message": "Project not found or you don't have permission to update it"
            }), 404
        
        return jsonify({
            "status": "success",
            "project": project
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500

@project_routes.route("/projects/<project_id>/shortlisted", methods=["POST"])
def add_shortlisted_image_to_project(project_id):
    """Add a shortlisted image to a project"""
    try:
        data = request.json
        image_id = data.get("image_id")
        
        if not image_id:
            return jsonify({
                "status": "error",
                "message": "Image ID is required"
            }), 400
        
        project = project_service.add_shortlisted_image_to_project(project_id, image_id)
        
        if not project:
            return jsonify({
                "status": "error",
                "message": "Project not found or you don't have permission to update it"
            }), 404
        
        return jsonify({
            "status": "success",
            "project": project
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500