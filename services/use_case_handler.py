# services/use_case_handler.py
from engines.factory import create_engine
from services.prompt_transformer import transform_prompt

class UseCaseHandler:
    """Handler for different use cases"""
    
    @staticmethod
    def handle_use_case(use_case, engine_name, prompt, image=None, options=None):
        """Handle a specific use case with the given engine"""
        
        # Create the engine
        engine = create_engine(engine_name)
        
        # Transform the prompt for the use case and engine
        transformed_prompt = transform_prompt(prompt, use_case, engine_name)
        
        # Extract the prompt string from the transformed object
        prompt_str = transformed_prompt.get("prompt", prompt)
        
        # Handle options merging
        if options is None:
            options = {}
        
        # Remove 'prompt' from transformed_prompt if it exists
        if "prompt" in transformed_prompt:
            del transformed_prompt["prompt"]
        
        # Merge remaining transformed options with provided options
        options.update(transformed_prompt)
        
        # Execute the appropriate method based on the use case
        if use_case == "text_to_image":
            return engine.text_to_image(prompt_str, options)
        
        elif use_case == "image_to_image":
            if image is None:
                raise ValueError("Image is required for image_to_image use case")
            return engine.image_to_image(prompt_str, image, options)
        
        elif use_case == "sketch_to_image":
            if image is None:
                raise ValueError("Sketch is required for sketch_to_image use case")
            return engine.sketch_to_image(prompt_str, image, options)
        
        elif use_case == "text_to_sketch":
            return engine.text_to_sketch(prompt_str, options)
        
        elif use_case == "image_to_sketch":
            if image is None:
                raise ValueError("Image is required for image_to_sketch use case")
            return engine.image_to_sketch(image, options)
        
        else:
            raise ValueError(f"Unsupported use case: {use_case}")