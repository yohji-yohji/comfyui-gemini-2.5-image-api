# ComfyUI Gemini API

A custom node for ComfyUI to integrate Google Gemini API for image generation.

## Installation

1. Clone this repository into your ComfyUI's `custom_nodes` directory:
   ```
   cd ComfyUI/custom_nodes
   git clone <repository-url>
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Restart ComfyUI

## Node Description

### Gemini 2.5 image

A node that generates images using the Gemini API.

**Input Parameters:**
- **prompt** (required): Text prompt describing the image you want to generate
- **api_key** (required): Your Google Gemini API key
- **model**: Model selection
- **aspect_ratio**: Choose image orientation (Free, Landscape, Portrait, Square)
- **temperature**: Parameter controlling generation diversity (0.0-2.0)
- **seed** (optional): Random seed for reproducible results
- **images** (optional): Reference image input, supports multiple images

**Outputs:**
- **image**: Generated image
- **API Respond**: Text information from API response

## Getting API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Create account and generate API key
3. Enter API key in the node

## Usage Notes

- Temperature range: 0.0 to 2.0
- Supports multiple reference images
- API may have usage limits, refer to Google's official documentation