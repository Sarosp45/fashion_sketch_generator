# Multi-Engine Image Generation API

A flexible API for generating images, sketches, tech packs, and size charts using multiple AI engines.

## Features

- **Multiple Engines**: Support for StabilityAI, OpenAI, and DALL-E.
- **Various Use Cases**: 
  - Text to Image
  - Image to Image
  - Sketch to Image
  - Text to Sketch
  - Image to Sketch
  - Tech Pack Generation
  - Size Chart Generation
- **Prompt Enhancement**: Automatic enhancement of user prompts for better results.
- **Flexible API**: Choose your engine and use case in the payload.

## Project Structure

```
engines/
  ├── __init__.py
  ├── base_engine.py         # Abstract base class for all engines
  ├── stability_engine.py    # StabilityAI implementation
  ├── openai_engine.py       # OpenAI implementation
  ├── dalle_engine.py        # DALL-E implementation
  └── factory.py             # Engine factory to create appropriate engine

services/
  ├── __init__.py
  ├── prompt_transformer.py  # Enhanced prompt transformation 
  └── use_case_handler.py    # Handles different use cases

routes/
  ├── __init__.py
  ├── image_routes.py        # Routes for image generation
  └── tech_pack_and_size_chart.py  # Routes for tech packs

utils/
  ├── __init__.py
  └── file_handler.py        # File handling utilities

config.py                    # Configuration
app.py                       # Main application
```

## API Endpoints

### Universal Image Generation Endpoint

```
POST /generate/create
```

This endpoint handles all image generation use cases. The payload structure is:

```json
{
  "prompt": "Your detailed prompt here",
  "use_case": "text_to_image",
  "engine": "stability_ai",
  "options": {
    "option1": "value1",
    "option2": "value2"
  }
}
```

For use cases requiring an image input (`image_to_image`, `sketch_to_image`, `image_to_sketch`), use form-data and include an image file with the key `image`.

### Legacy Endpoints (Maintained for Backwards Compatibility)

```
POST /generate/text-to-image
POST /generate/sketch-to-image
```

### Tech Pack and Size Chart Endpoints

```
POST /generate/tech-pack
POST /generate/size-chart
```

## Supported Use Cases

| Use Case | Description | Required Input | Supported Engines |
|----------|-------------|----------------|-------------------|
| `text_to_image` | Generate image from text | Prompt | stability_ai, openai, dall_e |
| `image_to_image` | Transform image based on text | Prompt, Image | stability_ai, openai, dall_e |
| `sketch_to_image` | Convert sketch to detailed image | Prompt, Image (sketch) | stability_ai, openai, dall_e |
| `text_to_sketch` | Generate sketch from text | Prompt | stability_ai, openai, dall_e |
| `image_to_sketch` | Convert image to sketch | Image | stability_ai, openai, dall_e |
| `tech_pack` | Generate apparel tech pack | Product type, Details | openai |
| `size_chart` | Generate apparel size chart | Product type, Region, Gender | openai |

## Supported Engines

- `stability_ai`: StabilityAI's image generation APIs
- `openai`: OpenAI's GPT-4 Vision and DALL-E 3
- `dall_e`: OpenAI's DALL-E 3 (specialized configuration)

## Quick Start

1. Install dependencies:
   ```
   pip install flask requests
   ```

2. Run the application:
   ```
   python app.py
   ```

3. Send a request:
   ```
   curl -X POST http://localhost:5000/generate/create \
     -H "Content-Type: application/json" \
     -d '{"prompt": "A beautiful mountain landscape at sunset", "use_case": "text_to_image", "engine": "stability_ai"}'
   ```

## Example Requests

### Text to Image with StabilityAI

```json
{
  "prompt": "A beautiful mountain landscape at sunset",
  "use_case": "text_to_image",
  "engine": "stability_ai"
}
```

### Sketch to Image with OpenAI

Use form-data with:
- `prompt`: "Convert this sketch to a detailed picture of a futuristic city"
- `use_case`: "sketch_to_image"
- `engine`: "openai"
- `image`: [upload sketch file]

### Generate Tech Pack

```json
{
  "product_type": "Men's Hoodie",
  "details": "Athletic fit, with kangaroo pocket and adjustable hood",
  "engine": "openai"
}
```

## Configuration

Update `config.py` to add or modify:
- API keys
- Default engine mappings
- Engine-specific options