import os
import base64
import torch
import numpy as np
from PIL import Image
import requests
from io import BytesIO

class GeminiImageGenerator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "api_key": ("STRING", {"default": "", "multiline": False}),
                "custom_base_url": ("STRING", {"default": "https://api.yoboxapp.com/gemini", "multiline": False}),
                "model": ("STRING", {"default": "gemini-2.5-flash-image-preview", "multiline": False}),
                "aspect_ratio": ([
                    "Free (自由比例)",
                    "Landscape (横屏)",
                    "Portrait (竖屏)",
                    "Square (方形)",
                ], {"default": "Free (自由比例)"}),
                "temperature": ("FLOAT", {"default": 1, "min": 0.0, "max": 2.0, "step": 0.05}),
            },
            "optional": {
                "seed": ("INT", {"default": 66666666, "min": 0, "max": 2147483647}),
                "image1": ("IMAGE",),
                "image2": ("IMAGE",),
                "image3": ("IMAGE",),
                "image4": ("IMAGE",),
                "image5": ("IMAGE",),
                "image6": ("IMAGE",),
                "image7": ("IMAGE",),
                "image8": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "API Respond")
    FUNCTION = "generate_image"
    CATEGORY = "Google-Gemini"
    
    def generate_image(self, prompt, api_key, custom_base_url, model, aspect_ratio, temperature, seed=66666666, image1=None, image2=None, image3=None, image4=None, image5=None, image6=None, image7=None, image8=None, **kwargs):
        """生成图像"""
        # 检查API密钥
        if not api_key or len(api_key) < 10:
            raise ValueError("错误: 未提供有效的API密钥")
        
        # 处理自定义URL
        base_url = custom_base_url.rstrip('/') if custom_base_url else "https://api.yoboxapp.com/gemini"
        
        # 处理种子值
        if seed == 0:
            import random
            seed = random.randint(1, 2**31 - 1)
        
        # 构建提示词
        if "Free" in aspect_ratio:
            simple_prompt = f"Create a detailed image of: {prompt}."
        elif "Landscape" in aspect_ratio:
            simple_prompt = f"Generate the image as a wide rectangular image where width is greater than height. Create a detailed image of: {prompt}."
        elif "Portrait" in aspect_ratio:
            simple_prompt = f"Generate the image as a tall rectangular image where height is greater than width. Create a detailed image of: {prompt}."
        else:  # Square
            simple_prompt = f"Generate the image as a square image where width equals height. Create a detailed image of: {prompt}."
        
        # 构建内容部分
        content_parts = [{"text": simple_prompt}]
        
        # 处理参考图像
        reference_count = 0
        images_list = [image1, image2, image3, image4, image5, image6, image7, image8]
        
        for idx, image in enumerate(images_list, 1):
            if image is not None:
                try:
                    # 如果是批量图像，只取第一张
                    if len(image.shape) == 4:  # 批量图像 [batch, height, width, channels]
                        input_image = image[0].cpu().numpy()
                    else:  # 单张图像 [height, width, channels]
                        input_image = image.cpu().numpy()
                    
                    input_image = (input_image * 255).astype(np.uint8)
                    pil_image = Image.fromarray(input_image)
                    
                    img_byte_arr = BytesIO()
                    pil_image.save(img_byte_arr, format='PNG')
                    img_byte_arr.seek(0)
                    image_bytes = img_byte_arr.read()
                    
                    image_b64 = base64.b64encode(image_bytes).decode('utf-8')
                    img_part = {"inlineData": {"mimeType": "image/png", "data": image_b64}}
                    content_parts.append(img_part)
                    reference_count += 1
                except Exception as e:
                    raise RuntimeError(f"处理第{idx}张参考图像时出错: {str(e)}")
        
        if reference_count > 0:
            suffix = " Use this reference image as guidance." if reference_count == 1 else f" Use these {reference_count} reference images as guidance."
            content_parts[0]["text"] += suffix
        
        # 构建请求数据
        contents = [{"role": "user", "parts": content_parts}]
        api_url = f"{base_url}/v1beta/models/{model}:generateContent"
        
        request_data = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "seed": seed,
                "response_modalities": ["Text", "Image"]
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        }
        
        # 发送请求
        try:
            response = requests.post(api_url, json=request_data, headers=headers, timeout=60)
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"网络请求失败: {str(e)}")
        
        if response.status_code != 200:
            raise RuntimeError(f"API请求失败，状态码: {response.status_code}, 响应: {response.text}")
        
        try:
            response_json = response.json()
        except Exception as e:
            raise RuntimeError(f"解析API响应失败: {str(e)}")
        
        if 'candidates' not in response_json or not response_json['candidates']:
            raise RuntimeError("API返回空响应，没有找到candidates")
        
        # 处理响应
        response_text = ""
        for part in response_json['candidates'][0]['content']['parts']:
            if 'text' in part and part['text']:
                response_text += part['text']
            
            elif 'inlineData' in part and part['inlineData']:
                inline_data = part['inlineData']
                image_data = inline_data.get('data', b'')
                
                if isinstance(image_data, str):
                    try:
                        image_data = base64.b64decode(image_data)
                    except Exception as e:
                        raise RuntimeError(f"Base64解码失败: {str(e)}")
                
                try:
                    buffer = BytesIO(image_data)
                    pil_image = Image.open(buffer)
                    
                    if pil_image.mode != 'RGB':
                        pil_image = pil_image.convert('RGB')
                    
                    img_array = np.array(pil_image).astype(np.float32) / 255.0
                    img_tensor = torch.from_numpy(img_array).unsqueeze(0)
                    
                    return (img_tensor, response_text if response_text else "图像生成成功")
                except Exception as e:
                    raise RuntimeError(f"图像处理失败: {str(e)}")
        
        # 如果没有找到图像数据
        if response_text:
            raise RuntimeError(f"API返回了文本但没有图像: {response_text}")
        else:
            raise RuntimeError("API没有返回任何图像或文本数据")

# 注册节点
NODE_CLASS_MAPPINGS = {
    "Google-Gemini": GeminiImageGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Google-Gemini": "Gemini 2.5 image"
}