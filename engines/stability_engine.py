import requests
from .base_engine import BaseEngine
from utils.file_handler import save_image

class StabilityEngine(BaseEngine):
    """StabilityAI implementation of the image generation engine"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "Accept": "image/*",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def _send_request(self, url, params, files=None):
        """Helper method to send requests to Stability API"""
        upload_files = {}
        if files:
            if 'image' in files and files['image']:
                upload_files['image'] = files['image']
            if 'mask' in files and files['mask']:
                upload_files['mask'] = files['mask']
        else:
            upload_files['none'] = ('', '')  # trick for multipart form if no actual files

        response = requests.post(
            url=url,
            headers=self.headers,
            data=params,
            files=upload_files
        )

        if not response.ok:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

        return response
    
    def text_to_image(self, prompt, options=None):
        """Generate an image from text using StabilityAI"""
        url = "https://api.stability.ai/v2beta/stable-image/generate/core"
        
        params = {
            "prompt": prompt,
            "mode": "text-to-image",
            "output_format": "png",
            "model": "stable-diffusion-v1-5"
        }
        
        # Merge with options if provided
        if options:
            params.update(options)
        
        response = self._send_request(url, params)
        return save_image(response.content, prefix="text_image")
    
    def sketch_to_image(self, prompt, sketch, options=None):
        """Convert a sketch to an image using StabilityAI"""
        url = "https://api.stability.ai/v2beta/stable-image/control/sketch"
        
        params = {
            "prompt": prompt,
            "output_format": "png",
            "mode": "image-to-image"
        }
        
        # Merge with options if provided
        if options:
            params.update(options)
        
        files = {"image": sketch}
        response = self._send_request(url, params, files)
        return save_image(response.content, prefix="sketch_image")
    
    def image_to_image(self, prompt, image, options=None):
        """Transform an image based on text prompt using StabilityAI"""
        url = "https://api.stability.ai/v2beta/stable-image/generate/core"
        
        params = {
            "prompt": prompt,
            "mode": "image-to-image",
            "output_format": "png",
            "model": "stable-diffusion-v1-5"
        }
        
        # Merge with options if provided
        if options:
            params.update(options)
        
        files = {"image": image}
        response = self._send_request(url, params, files)
        return save_image(response.content, prefix="image_to_image")
    
    def text_to_sketch(self, prompt, options=None):
        """Generate a sketch from text using StabilityAI"""
        # StabilityAI doesn't have a direct text-to-sketch endpoint
        # This is a workaround using text-to-image with sketch-like settings
        url = "https://api.stability.ai/v2beta/stable-image/generate/core"
        
        params = {
            "prompt": f"sketch drawing of {prompt}, line art, black and white, minimal",
            "mode": "text-to-image",
            "output_format": "png",
            "model": "stable-diffusion-v1-5"
        }
        
        # Merge with options if provided
        if options:
            params.update(options)
        
        response = self._send_request(url, params)
        return save_image(response.content, prefix="text_sketch")
    
    def image_to_sketch(self, image, options=None):
        """Convert an image to a sketch using StabilityAI"""
        # StabilityAI doesn't have a direct image-to-sketch endpoint
        # This is a workaround using img2img with sketch-like settings
        url = "https://api.stability.ai/v2beta/stable-image/generate/core"
        
        params = {
            "prompt": "convert to sketch, line art, black and white, minimal",
            "mode": "image-to-image",
            "output_format": "png",
            "model": "stable-diffusion-v1-5"
        }
        
        # Merge with options if provided
        if options:
            params.update(options)
        
        files = {"image": image}
        response = self._send_request(url, params, files)
        return save_image(response.content, prefix="image_sketch")