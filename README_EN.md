# ComfyUI Gemini 2.5 Image Generation Plugin

A specialized ComfyUI node for Gemini 2.5 image generation, supporting both text prompts and reference image guidance for high-quality image creation.

## ✨ Key Features

- 🎨 Pure text-to-image generation
- 🖼️ Support for up to 8 reference images as guidance
- 📐 Flexible aspect ratio control (Free, Landscape, Portrait, Square)
- 🛠️ Customizable API endpoints
- 🌡️ Temperature parameter for creativity control
- 🎯 Seed value for reproducible results
- 🌍 Full Chinese interface support

## 📦 Installation

1. **Clone repository to ComfyUI plugin directory**
   ```bash
   cd ComfyUI/custom_nodes
   git clone https://github.com/yohji-yohji/comfyui-gemini-2.5-image-api.git
   ```

2. **Install dependencies**
   ```bash
   pip install requests pillow torch numpy
   ```

3. **Restart ComfyUI**

## 🔑 API Key Acquisition

Visit [https://api.yoboxapp.com/](https://api.yoboxapp.com/) to apply for and manage your API keys.

## 🚀 Detailed Node Description

### Gemini 2.5 image

**Required Parameters:**
- **prompt** (text): Detailed description of the image content you want to generate
- **api_key** (text): API key obtained from yoboxapp.com

**Optional Parameters:**
- **custom_base_url** (text): Custom API endpoint, defaults to `https://api.yoboxapp.com/gemini`
- **model** (text): Model name, defaults to `gemini-2.5-flash-image-preview`
- **aspect_ratio** (dropdown):
  - `Free (自由比例)` - No aspect ratio restrictions
  - `Landscape (横屏)` - Generate landscape images with width > height
  - `Portrait (竖屏)` - Generate portrait images with height > width
  - `Square (方形)` - Generate square images with equal width and height
- **temperature** (float): Creativity control, range 0.0-2.0, default 1.0
- **seed** (integer): Random seed, default 66666666, set to 0 for random generation
- **image1-image8** (image): Up to 8 reference image inputs

**Outputs:**
- **image**: Generated image tensor
- **API Respond**: API response text

## 💡 Usage Tips

1. **Prompt Optimization**
   - Use detailed, specific descriptions
   - Include style, color, and composition elements
   - Avoid overly complex or contradictory descriptions

2. **Reference Images**
   - Upload 1-8 reference images
   - Reference images serve as style and content guidance
   - System automatically adds guidance text

3. **Aspect Ratio Control**
   - Choose appropriate ratios based on purpose
   - Landscape works best for scenery and landscapes
   - Portrait works best for portraits and posters

4. **Parameter Adjustment**
   - Lower temperature (0.1-0.5): More stable and consistent results
   - Higher temperature (1.0-2.0): More creative and varied results
   - Use fixed seed to reproduce identical results

## ⚠️ Important Notes

- Ensure API key is valid and has sufficient quota
- Large image generation may require more time
- Network timeout set to 60 seconds, please be patient for complex images
- Reference images are automatically converted to PNG format
- If errors occur, check network connection and API key status

## 🔧 Troubleshooting

**Common errors and solutions:**

- `错误: 未提供有效的API密钥` - Please check if API key is correctly entered
- `网络请求失败` - Check network connection or try different API endpoint
- `API请求失败` - Check API key quota or service status
- `图像处理失败` - Ensure reference image formats are correct

## 📄 Changelog

- Support for Gemini 2.5 model
- Multiple reference image input functionality
- Precise aspect ratio control
- Chinese interface and error messages
- Custom API endpoint support

## 🤝 Contributing & Feedback

For issues or suggestions, welcome to submit Issues or Pull Requests.