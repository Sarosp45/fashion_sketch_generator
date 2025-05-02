
from .stability_engine import StabilityEngine
from .openai_engine import OpenAIEngine
from .dalle_engine import DALLEEngine
from utils.logger import *
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEYS = {
    "stability_ai": os.getenv("STABILITY_API_KEY"),
    "modelslab": os.getenv("MODELSLAB_API_KEY"),
    "openai": os.getenv("OPENAI_API_KEY"),
    "dall_e": os.getenv("OPENAI_API_KEY")  # DALL·E shares OpenAI key
}

# Supported engines and use cases
SUPPORTED_ENGINES = list(API_KEYS.keys())

def create_engine(engine_name):
    """Factory function to create the appropriate engine"""
    engines = {
        "stability_ai": StabilityEngine,
        "openai": OpenAIEngine,
        "dall_e": DALLEEngine
    }
    
    if engine_name not in engines:
        raise ValueError(f"Unsupported engine: {engine_name}")
    
    if engine_name not in API_KEYS:
        raise ValueError(f"No API key found for engine: {engine_name}")
    

    eval_logger.info("Engine for this case:", engine_name)

    return engines[engine_name](API_KEYS[engine_name])