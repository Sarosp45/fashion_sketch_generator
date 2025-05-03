
import uuid
import time

class Project:
    """Project model for organizing user's work"""
    def __init__(self, name, description=None, user_id=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.user_id = user_id
        self.created_at = time.time()
        self.updated_at = time.time()
        self.prompts = []  # List of prompt IDs associated with this project
        self.shortlisted_images = []  # List of shortlisted image IDs for this project
        self.metadata = {}  # Additional project metadata
    
    def add_prompt(self, prompt_id):
        """Add a prompt to the project"""
        if prompt_id not in self.prompts:
            self.prompts.append(prompt_id)
            self.updated_at = time.time()
        return self.prompts
    
    def add_shortlisted_image(self, image_id):
        """Add a shortlisted image to the project"""
        if image_id not in self.shortlisted_images:
            self.shortlisted_images.append(image_id)
            self.updated_at = time.time()
        return self.shortlisted_images
    
    def remove_prompt(self, prompt_id):
        """Remove a prompt from the project"""
        if prompt_id in self.prompts:
            self.prompts.remove(prompt_id)
            self.updated_at = time.time()
        return self.prompts
    
    def remove_shortlisted_image(self, image_id):
        """Remove a shortlisted image from the project"""
        if image_id in self.shortlisted_images:
            self.shortlisted_images.remove(image_id)
            self.updated_at = time.time()
        return self.shortlisted_images
    
    def update_metadata(self, metadata):
        """Update project metadata"""
        self.metadata.update(metadata)
        self.updated_at = time.time()
        return self.metadata
    
    def to_dict(self):
        """Convert project to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'prompts': self.prompts,
            'shortlisted_images': self.shortlisted_images,
            'metadata': self.metadata
        }