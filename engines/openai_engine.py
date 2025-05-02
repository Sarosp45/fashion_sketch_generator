# engines/openai_engine.py
import requests
import json
import base64
from io import BytesIO
from .base_engine import BaseEngine
from utils.file_handler import save_image

class OpenAIEngine(BaseEngine):
    """OpenAI implementation of the image generation engine"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.base_url = "https://api.openai.com/v1"
    
    def _encode_image(self, image_file):
        """Encode image file to base64"""
        if hasattr(image_file, 'read'):
            # If it's a file-like object
            image_data = image_file.read()
        else:
            # If it's already bytes
            image_data = image_file
            
        return base64.b64encode(image_data).decode('utf-8')
    
    def text_to_image(self, prompt, options=None):
        """Generate an image from text using OpenAI DALL-E 3"""
        url = f"{self.base_url}/images/generations"
        
        # Define allowed parameters for the OpenAI image generations API
        allowed_params = {
            "model", "prompt", "n", "size", "quality", 
            "response_format", "style", "user"
        }
        
        # Start with default payload
        payload = {
            "model": "dall-e-3",
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024",
            "quality": "standard",
            "response_format": "b64_json"
        }
        
        # Only add allowed parameters from options
        if options:
            filtered_options = {k: v for k, v in options.items() if k in allowed_params}
            payload.update(filtered_options)
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if not response.ok:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        result = response.json()
        image_data = base64.b64decode(result["data"][0]["b64_json"])
        return save_image(image_data, prefix="openai_text_image")
    
    def image_to_image(self, prompt, image, options=None):
        """Transform an image based on text prompt using OpenAI"""
        url = f"{self.base_url}/images/variations"
        
        # Define allowed parameters for the OpenAI image variations API
        allowed_params = {
            "model", "image", "prompt", "n", "size", 
            "response_format", "user"
        }
        
        # OpenAI requires image files in base64 format
        image_base64 = self._encode_image(image)
        
        # Start with default payload
        payload = {
            "model": "dall-e-3",
            "image": image_base64,
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024",
            "response_format": "b64_json"
        }
        
        # Only add allowed parameters from options
        if options:
            filtered_options = {k: v for k, v in options.items() if k in allowed_params}
            payload.update(filtered_options)
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if not response.ok:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        result = response.json()
        image_data = base64.b64decode(result["data"][0]["b64_json"])
        return save_image(image_data, prefix="openai_image_to_image")
    
    def sketch_to_image(self, prompt, sketch, options=None):
        """Convert a sketch to an image using OpenAI"""
        # OpenAI doesn't have a specific sketch-to-image API
        # Use the image variation API with a prompt
        return self.image_to_image(prompt, sketch, options)
    
    def text_to_sketch(self, prompt, options=None):
        """Generate a sketch from text using OpenAI"""
        # Modify the prompt to specifically request a sketch
        sketch_prompt = f"Create a detailed sketch/line art drawing of: {prompt}. Black and white, line art only, no shading or color."
        return self.text_to_image(sketch_prompt, options)
    
    def image_to_sketch(self, image, options=None):
        """Convert a fashion image to a sketch using GPT-4 Vision + DALL·E"""
    # Step 1: Describe the fashion image using GPT-4 Vision
        url = f"{self.base_url}/chat/completions"

        image_base64 = self._encode_image(image)

        payload = {
            "model": "gpt-4-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Analyze this fashion image and describe it as a sketch outline. "
                                "Focus only on garment structure, silhouette, stitching, and key fashion elements. "
                                "Avoid colors, textures, and unnecessary background details."
                            )
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 500
        }

        if options:
            filtered_options = {k: v for k, v in options.items()
                                if k in ["model", "max_tokens", "temperature", "top_p"]}
            payload.update(filtered_options)

        response = requests.post(url, headers=self.headers, json=payload)
        
        if not response.ok:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        description = response.json()["choices"][0]["message"]["content"]

        # Step 2: Use DALL·E to generate a sketch from the description
        sketch_prompt = (
            f"Create a clean black and white sketch/line art based on the following fashion description:\n{description}.\n"
            "Focus on silhouette, seams, and garment features only. No color or shading."
        )
        return self.text_to_image(sketch_prompt, options)
