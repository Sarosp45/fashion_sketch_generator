# engines/dalle_engine.py
import requests
import json
import base64
from io import BytesIO
from .base_engine import BaseEngine
from utils.file_handler import save_image

class DALLEEngine(BaseEngine):
    """DALL-E implementation of the image generation engine"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        # For this example, we're using OpenAI's API for DALL-E
        # In a real implementation, this might be a separate service
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
        """Generate an image from text using DALL-E"""
        url = f"{self.base_url}/images/generations"
        
        payload = {
            "model": "dall-e-3",
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024",
            "response_format": "b64_json"
        }
        
        # Merge with options if provided
        if options:
            payload.update(options)
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if not response.ok:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        result = response.json()
        image_data = base64.b64decode(result["data"][0]["b64_json"])
        return save_image(image_data, prefix="dalle_text_image")
    
    def image_to_image(self, prompt, image, options=None):
        """Transform an image based on text prompt using DALL-E"""
        # DALL-E 3 doesn't directly support image-to-image
        # We'll use a combination of image analysis and generation
        
        # First, analyze the image using GPT-4 Vision
        vision_url = f"{self.base_url}/chat/completions"
        image_base64 = self._encode_image(image)
        
        vision_payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": f"Describe this image in detail, focusing on elements mentioned in this prompt: {prompt}"
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
            "max_tokens": 300
        }
        
        vision_response = requests.post(vision_url, headers=self.headers, json=vision_payload)
        
        if not vision_response.ok:
            raise Exception(f"HTTP {vision_response.status_code}: {vision_response.text}")
        
        vision_result = vision_response.json()
        image_description = vision_result["choices"][0]["message"]["content"]
        
        # Now generate a new image based on the description and original prompt
        enhanced_prompt = f"{prompt}. Based on an image with: {image_description}"
        return self.text_to_image(enhanced_prompt, options)
    
    def sketch_to_image(self, prompt, sketch, options=None):
        """Convert a sketch to an image using DALL-E"""
        # Similar approach to image_to_image
        return self.image_to_image(f"Convert this sketch into a detailed image. {prompt}", sketch, options)
    
    def text_to_sketch(self, prompt, options=None):
        """Generate a sketch from text using DALL-E"""
        sketch_prompt = f"Create a detailed black and white sketch/line art of {prompt}. Only outlines, no shading, no color."
        return self.text_to_image(sketch_prompt, options)
    
    def image_to_sketch(self, image, options=None):
        """Convert an image to a sketch using DALL-E"""
        # First, analyze the image
        vision_url = f"{self.base_url}/chat/completions"
        image_base64 = self._encode_image(image)
        
        vision_payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": "Describe this image in detail, focusing on shapes, outlines, and key features."
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
            "max_tokens": 300
        }
        
        vision_response = requests.post(vision_url, headers=self.headers, json=vision_payload)
        
        if not vision_response.ok:
            raise Exception(f"HTTP {vision_response.status_code}: {vision_response.text}")
        
        vision_result = vision_response.json()
        image_description = vision_result["choices"][0]["message"]["content"]
        
        # Now generate a sketch based on the description
        sketch_prompt = f"Create a simple line art sketch of: {image_description}. Black and white outlines only, no shading or color."
        return self.text_to_image(sketch_prompt, options)