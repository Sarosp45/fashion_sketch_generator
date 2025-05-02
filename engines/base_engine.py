from abc import ABC, abstractmethod

class BaseEngine(ABC):
    """Abstract base class for all image generation engines"""
    
    @abstractmethod
    def text_to_image(self, prompt, options=None):
        """Generate an image from text"""
        pass
    
    @abstractmethod
    def image_to_image(self, prompt, image, options=None):
        """Transform an image based on text prompt"""
        pass
    
    @abstractmethod
    def sketch_to_image(self, prompt, sketch, options=None):
        """Convert a sketch to an image"""
        pass
    
    @abstractmethod
    def text_to_sketch(self, prompt, options=None):
        """Generate a sketch from text"""
        pass
    
    @abstractmethod
    def image_to_sketch(self, image, options=None):
        """Convert an image to a sketch"""
        pass