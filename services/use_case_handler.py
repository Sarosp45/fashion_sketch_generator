from engines.factory import create_engine
from services.prompt_transformer import transform_prompt, ai_enhance_prompt
from services.user_services import user_service
from utils.logger import *

class UseCaseHandler:
    """Handles different image generation use cases"""
    
    @staticmethod
    def handle_use_case(use_case, engine_name, prompt, image=None, options=None):
        """Handle different image generation use cases with user tracking"""
        # Check if prompt needs enhancement due to multiple regenerations
        if user_service.should_enhance_prompt(prompt, use_case):
            # Log that we're enhancing the prompt
            eval_logger.info(f"Enhancing prompt after multiple regenerations: {prompt}")
            # Use GPT-4 to enhance the prompt
            prompt = ai_enhance_prompt(prompt, use_case)
            eval_logger.info(f"Enhanced prompt: {prompt}")
        
        # Transform the prompt based on use case and engine
        transformed_options = transform_prompt(prompt, use_case, engine_name)
        
        # Merge with additional options if provided
        if options:
            transformed_options.update(options)
        
        # Create the appropriate engine
        engine = create_engine(engine_name)
        
        # Handle specific use case
        if use_case == "text_to_image":
            image_path = engine.text_to_image(prompt, transformed_options)
        elif use_case == "image_to_image":
            if not image:
                raise ValueError("Image is required for image-to-image transformation")
            image_path = engine.image_to_image(prompt, image, transformed_options)
        elif use_case == "sketch_to_image":
            if not image:
                raise ValueError("Sketch image is required for sketch-to-image transformation")
            image_path = engine.sketch_to_image(prompt, image, transformed_options)
        elif use_case == "text_to_sketch":
            image_path = engine.text_to_sketch(prompt, transformed_options)
        elif use_case == "image_to_sketch":
            if not image:
                raise ValueError("Image is required for image-to-sketch transformation")
            image_path = engine.image_to_sketch(image, transformed_options)
        else:
            raise ValueError(f"Unsupported use case: {use_case}")
        
        # Track the prompt and result in user history
        prompt_data = user_service.track_prompt(
            prompt=prompt,
            use_case=use_case,
            engine=engine_name,
            image_path=image_path
        )
        
        return image_path, prompt_data['id']