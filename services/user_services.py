
from models.user import User
import uuid
from flask import session
import time

class UserService:
    """Service to manage users and their sessions"""
    def __init__(self):
        self.users = {}  # In-memory store of User objects
    
    def get_current_user(self):
        """Get current user from session or create a new one"""
        user_id = session.get('user_id')
        
        if not user_id:
            # Create a new user if none exists
            user_id = str(uuid.uuid4())
            session['user_id'] = user_id
            self.users[user_id] = User(user_id)
        
        # Get or create user in memory
        if user_id not in self.users:
            self.users[user_id] = User(user_id)
            
        return self.users[user_id]
    
    def track_prompt(self, prompt, use_case, engine, image_path=None):
        """Track a prompt in the user's history"""
        user = self.get_current_user()
        
        prompt_id = str(uuid.uuid4())
        prompt_data = {
            'id': prompt_id,
            'prompt': prompt,
            'use_case': use_case,
            'engine': engine,
            'timestamp': time.time(),
            'image_path': image_path,
            'regeneration_count': 0  # Track how many times this prompt was regenerated
        }
        
        user.add_prompt(prompt_data)
        return prompt_data
    
    def should_enhance_prompt(self, prompt, use_case):
        """Check if a prompt needs enhancement based on history"""
        user = self.get_current_user()
        
        # Count how many times this exact prompt was used
        regeneration_count = 0
        for p in user.prompt_history:
            if p['prompt'] == prompt and p['use_case'] == use_case:
                regeneration_count += 1
                # Update the regeneration count for this prompt
                p['regeneration_count'] += 1
        
        # If regenerated more than 5 times, suggest enhancement
        return regeneration_count >= 5
    
    def shortlist_image(self, image_path, prompt_id):
        """Add an image to user's shortlist"""
        user = self.get_current_user()
        
        image_id = str(uuid.uuid4())
        image_data = {
            'id': image_id,
            'image_path': image_path,
            'prompt_id': prompt_id,
            'timestamp': time.time()
        }
        
        user.shortlist_image(image_data)
        return image_data
    
    def save_feedback(self, prompt_id, rating, comments=None):
        """Save user feedback for a prompt"""
        user = self.get_current_user()
        
        feedback_data = {
            'rating': rating,
            'comments': comments,
            'timestamp': time.time()
        }
        
        user.add_feedback(prompt_id, feedback_data)
        return feedback_data
    
    def get_prompt_history(self):
        """Get current user's prompt history"""
        user = self.get_current_user()
        return user.prompt_history
    
    def get_shortlisted_images(self):
        """Get current user's shortlisted images"""
        user = self.get_current_user()
        return user.shortlisted_images

# Create a global instance of UserService
user_service = UserService()