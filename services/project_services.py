
from models.project_models import Project
from services.user_services import user_service
import time

class ProjectService:
    """Service to manage projects"""
    def __init__(self):
        self.projects = {}  # In-memory store of Project objects
    
    def create_project(self, name, description=None):
        """Create a new project for the current user"""
        user = user_service.get_current_user()
        
        # Create a new project
        project = Project(
            name=name,
            description=description,
            user_id=user.user_id
        )
        
        # Store the project
        self.projects[project.id] = project
        
        # Link project to user
        user.add_project(project.id, project.to_dict())
        
        return project.to_dict()
    
    def get_project(self, project_id):
        """Get a project by ID"""
        project = self.projects.get(project_id)
        if project:
            return project.to_dict()
        return None
    
    def get_user_projects(self):
        """Get all projects for the current user"""
        user = user_service.get_current_user()
        
        user_projects = []
        for project_id, project in self.projects.items():
            if project.user_id == user.user_id:
                user_projects.append(project.to_dict())
        
        return user_projects
    
    def update_project(self, project_id, name=None, description=None, metadata=None):
        """Update a project"""
        project = self.projects.get(project_id)
        user = user_service.get_current_user()
        
        if not project or project.user_id != user.user_id:
            return None
        
        if name:
            project.name = name
        
        if description:
            project.description = description
        
        if metadata:
            project.update_metadata(metadata)
        
        project.updated_at = time.time()
        
        # Update in user's projects
        user.add_project(project.id, project.to_dict())
        
        return project.to_dict()
    
    def delete_project(self, project_id):
        """Delete a project"""
        project = self.projects.get(project_id)
        user = user_service.get_current_user()
        
        if not project or project.user_id != user.user_id:
            return False
        
        # Remove from projects dictionary
        del self.projects[project_id]
        
        # Remove from user's projects
        if project_id in user.projects:
            del user.projects[project_id]
        
        return True
    
    def add_prompt_to_project(self, project_id, prompt_id):
        """Add a prompt to a project"""
        project = self.projects.get(project_id)
        user = user_service.get_current_user()
        
        if not project or project.user_id != user.user_id:
            return None
        
        project.add_prompt(prompt_id)
        
        # Update in user's projects
        user.add_project(project.id, project.to_dict())
        
        return project.to_dict()
    
    def add_shortlisted_image_to_project(self, project_id, image_id):
        """Add a shortlisted image to a project"""
        project = self.projects.get(project_id)
        user = user_service.get_current_user()
        
        if not project or project.user_id != user.user_id:
            return None
        
        project.add_shortlisted_image(image_id)
        
        # Update in user's projects
        user.add_project(project.id, project.to_dict())
        
        return project.to_dict()

# Create a global instance of ProjectService
project_service = ProjectService()