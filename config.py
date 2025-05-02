import os


# Engine mapping for different use cases (default engines)
USE_CASE_ENGINE_MAPPING = {
    "text_to_image": "stability_ai",
    "sketch_to_image": "stability_ai",
    "image_to_image": "stability_ai",
    "text_to_sketch": "openai",
    "image_to_sketch": "openai",
    "size_chart": "openai",
    "tech_pack": "openai"
}


SUPPORTED_USE_CASES = [
    "text_to_image",
    "sketch_to_image",
    "image_to_image",
    "text_to_sketch",
    "image_to_sketch",
    "size_chart",
    "tech_pack"
]

DEFAULT_ENGINE_OPTIONS = {
    "stability_ai": {
        "output_format": "png",
        "seed": 0
    },
    "openai": {
        "size": "1024x1024",
        "n": 1,
        "quality": "standard"
    },
    "dall_e": {
        "size": "1024x1024",
        "n": 1,
        "quality": "standard"
    }
}
