# services/prompt_transformer.py
import requests
import json
from utils.logger import *
import sys
import openai

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEYS = os.getenv("OPENAI_API_KEY")


def enhance_prompt(prompt, use_case):
    """Enhance user prompt tailored for the Indian garment/textile industry"""

    enhancement_map = {
        "text_to_image": (
            "Create a simple garment sketch on a plain white background. "
            "Use pencil lines only, no colors or digital effects. Show"
        ),
        "sketch_to_image": (
            "Convert this pencil garment sketch into a realistic image. "
            "Keep original shape and structure. Use soft natural lighting and a plain white background. Show"
        ),
        "image_to_image": (
            "Convert this image into a garment sketch. Use clean pencil lines on a white background. "
            "No color or shading. Focus on fabric lines and basic shape. Show"
        ),
        "text_to_sketch": (
            "Draw a pencil sketch of a single garment on a white background. "
            "No colors or shading. Keep it simple and clear. Show"
        ),
        "image_to_sketch": (
            "Convert this image into a clear pencil garment sketch. "
            "No shading or effects. Use white background and focus on garment structure."
        )
    }

    enhancement = enhancement_map.get(use_case, "")
    if not enhancement:
        return prompt

    if prompt.lower().startswith(enhancement.lower()):
        return prompt

    return f"{enhancement} {prompt}"


def sanitize_prompt_for_moderation(prompt: str) -> str:
    """Remove terms that may trigger filters, keeping garment intent clear."""
    risky_terms = {
        "corset": "structured upper panel",
        "fitted skirt": "narrow bottom section",
        "back view": "rear garment view",
        "bare back": "open-back style",
        "transparent": "semi-sheer",
        "see-through": "semi-sheer",
        "nude": "neutral tone",
        "lingerie": "inner garment",
        "cleavage": "deep neckline",
        "tight": "close-fitting"
    }

    for term, replacement in risky_terms.items():
        prompt = prompt.replace(term, replacement)
    return prompt

import openai
import requests

def ai_enhance_prompt(prompt, use_case):
    """Use OpenAI to enhance a prompt for garment-focused image generation."""
    
    # Fallback if API key is not available
    if "openai" not in API_KEYS:
        return enhance_prompt(prompt, use_case)

    api_key = API_KEYS["openai"]
    openai.api_key = api_key

    system_prompts = {
        "text_to_image": (
            "You are a garment design assistant for textile and manufacturing use. "
            "Return only the prompt to generate a simple garment sketch in pencil lines on a plain white background. "
            "No colors, no shading, no digital effects. The sketch should clearly show garment structure for catalog or sampling use."
        ),
        "sketch_to_image": (
            "You are a garment prompt expert converting sketches into realistic images for catalog or product views. "
            "Return only the final image prompt. Keep natural lighting, white background, and match the sketch structure exactly. "
            "No digital art or styling. The result should show the garment as-is, clearly."
        ),
        "image_to_image": (
            "You are a garment sketch expert. Convert any image into a simple black pencil sketch showing garment outlines only. "
            "Plain white background. No color, effects, or complex details. Keep it clear and manufacturing-friendly."
        ),
        "text_to_sketch": (
            "You are a garment assistant generating pencil sketches from text prompts. "
            "Return only a clean prompt for sketching the garment in plain lines. No shading, colors, or extra details as like a human hand drawn Sketchout. "
            "White background. This is for production use, not fashion illustration."
        ),
        "image_to_sketch": (
            "You are a garment design assistant creating simple pencil sketches from garment photos. "
            "Use clean black pencil lines only. White background. No styling, effects, or fashion elements. Just the garment structure."
        )
    }

    # Select system prompt or fallback to empty string
    system_prompt = system_prompts.get(use_case, "")
    sanitized_prompt = sanitize_prompt_for_moderation(prompt)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=0.7,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": sanitized_prompt}
            ]
        )
        enhanced_prompt = response["choices"][0]["message"]["content"].strip()
        return enhanced_prompt

    except Exception as e:
        print(f"[OpenAI API Error]: {e}")
        # Fallback to local method if API fails
        return enhance_prompt(prompt, use_case)



# def ai_enhance_prompt(prompt, use_case):
#     """Use OpenAI to enhance a sanitized prompt, producing a final image-generation-ready output"""

#     if "openai" not in API_KEYS:
#         return enhance_prompt(prompt, use_case)

#     api_key = API_KEYS["openai"]
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json"
#     }

#     system_prompts = {
#             "text_to_image": (
#                 "You are a fashion design AI that creates final prompts for generating hand-drawn pencil sketch fashion illustrations. "
#                 "Return ONLY the full image prompt with no extra explanation or instruction. "
#                 "The result must look like a designer’s final concept sketch: clean black-and-white, pencil-only, plain white background, no colors, no shading. "
#                 "**STRICTLY NO DIGITAL ART**. "
#                 "Ensure the design resembles a traditional fashion designer’s pencil sketch, with no digital manipulation or effects. "
#                 "**NO BACKGROUNDS EXCEPT PLAIN WHITE**. Terms like 'runway show' should bever be used"
#             ),
#             "sketch_to_image": (
#                 "You are a fashion design AI that writes prompts to convert sketches into photorealistic fashion images. "
#                 "Return ONLY the final image-generation prompt with no instructions. It should describe a realistic full-body garment image "
#                 "with natural lighting, neutral background, and true-to-sketch structure. "
#                 "**STRICTLY NO DIGITAL ART EFFECTS**. Terms like 'runway show' should bever be used"
#             ),
#             "image_to_image": (
#                 "You are a prompt expert for converting fashion images into clean hand-drawn-style sketches. "
#                 "Return ONLY the final image prompt: pencil-only sketch on a plain white background, no color, shading, or digital effects. "
#                 "**STRICTLY NO DIGITAL ART**. The sketch must resemble a traditional hand-drawn pencil fashion sketch, no digital effects allowed."
#                 "Terms like 'runway show' should bever be used"
#             ),
#             "text_to_sketch": (
#                 "You are a fashion design AI generating prompts to create pencil sketch illustrations. "
#                 "Return ONLY the clean, final image-generation prompt in pencil sketch format, plain white background, no colors, no effects. "
#                 "Ensure the sketch is in traditional hand-drawn pencil style with NO digital manipulation. "
#                 "Terms like 'runway show' should bever be used"
#                 "**STRICTLY NO DIGITAL ART**. The sketch must resemble a traditional hand-drawn pencil fashion sketch, no digital effects allowed."
#             ),
#             "image_to_sketch": (
#                 "You are a fashion design AI that converts fashion photos into sketch prompts. "
#                 "Return ONLY the final prompt for a line-art sketch, black and white, plain white background, showing garment structure only. "
#                 "Ensure the sketch looks like a traditional pencil sketch with NO digital effects. "
#                 "Terms like 'runway show' should bever be used"
#                 "**STRICTLY NO DIGITAL ART**. The sketch must resemble a traditional hand-drawn pencil fashion sketch, no digital effects allowed."
#             )
#         }


#     system_prompt = system_prompts.get(use_case, "You are a prompt engineer that returns a final, single-line prompt for fashion image generation.")

#     # 🔒 Step 1: sanitize input
#     sanitized_prompt = sanitize_prompt_for_moderation(prompt)

#     # 🔁 Step 2: Call OpenAI API
#     url = "https://api.openai.com/v1/chat/completions"
#     payload = {
#         "model": "gpt-4-turbo",
#         "messages": [
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": sanitized_prompt}
#         ],
#         "max_tokens": 150,
#         "temperature": 0.7
#     }

#     try:
#         response = requests.post(url, headers=headers, json=payload)
#         if not response.ok:
#             return enhance_prompt(prompt, use_case)

#         result = response.json()
#         enhanced_prompt = result["choices"][0]["message"]["content"].strip()

#         # Ensure no extra content beyond the prompt
#         if "\n" in enhanced_prompt:
#             lines = [line.strip() for line in enhanced_prompt.split("\n") if line.strip()]
#             enhanced_prompt = lines[-1]  # Keep only final descriptive line

#         return enhanced_prompt

#     except Exception as e:
#         print(f"Error in AI prompt enhancement: {str(e)}")
#         print("Enhanced Prompt (fallback):", prompt)
#         return enhance_prompt(prompt, use_case)

def transform_prompt(prompt, use_case, engine):
    """Transform the prompt using OpenAI if available, else fallback to manual enhancement."""
    if "openai" in API_KEYS:
        try:
            enhanced_prompt = ai_enhance_prompt(prompt, use_case)
        except Exception as e:
            print(f"[WARN] OpenAI prompt enhancement failed: {e}")
            enhanced_prompt = enhance_prompt(prompt, use_case)
    else:
        enhanced_prompt = enhance_prompt(prompt, use_case)

    print(">>> [DEBUG] Enhanced Prompt Used for Generation:")
    print(enhanced_prompt)
    sys.stdout.flush()

    if engine == "stability_ai":
        return {
            "prompt": enhanced_prompt,
            "seed": 0,
            "output_format": "png"
        }
    elif engine in ("openai", "dall_e"):
        return {
            "prompt": enhanced_prompt,
            "n": 1,
            "size": "1024x1024"
        }

    print("Final prompt:", enhanced_prompt, "\n")
    return {"prompt": enhanced_prompt}


