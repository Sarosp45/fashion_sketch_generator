
class User:
    """User model for session management"""
    def __init__(self, user_id, username=None, email=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.prompt_history = []  # Track prompt history
        self.shortlisted_images = []  # Track shortlisted images
        self.projects = {}  # Map of project_id -> project_data
        self.feedback_history = []  # Track feedback for prompts
        
    def add_prompt(self, prompt_data):
        """Add a prompt to user history, maintaining max 5 entries"""
        self.prompt_history.insert(0, prompt_data)  # Add to the beginning
        if len(self.prompt_history) > 5:
            self.prompt_history.pop()  # Remove oldest prompt if exceeding 5
        return self.prompt_history
    
    def shortlist_image(self, image_data):
        """Add an image to shortlist"""
        self.shortlisted_images.append(image_data)
        return self.shortlisted_images
    
    def remove_shortlisted_image(self, image_id):
        """Remove an image from shortlist"""
        self.shortlisted_images = [img for img in self.shortlisted_images if img['id'] != image_id]
        return self.shortlisted_images
    
    def add_project(self, project_id, project_data):
        """Add or update a project"""
        self.projects[project_id] = project_data
        return self.projects
    
    def add_feedback(self, prompt_id, feedback_data):
        """Add feedback for a prompt"""
        self.feedback_history.append({
            'prompt_id': prompt_id,
            'feedback': feedback_data
        })
        return self.feedback_history