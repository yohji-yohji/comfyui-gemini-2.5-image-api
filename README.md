# ComfyUI Gemini API

用于在ComfyUI中调用Google Gemini API生成图像的节点。

## 安装说明

1. 将此存储库克隆到ComfyUI的`custom_nodes`目录：
   ```
   cd ComfyUI/custom_nodes
   git clone <repository-url>
   ```

2. 安装所需依赖：
   ```
   pip install -r requirements.txt
   ```

3. 重启ComfyUI

## 节点说明

### Gemini 2.5 image

通过Gemini API生成图像的节点。

**输入参数：**
- **prompt** (必填)：描述你想要生成的图像的文本提示词
- **api_key** (必填)：你的Google Gemini API密钥
- **model**：模型选择
- **aspect_ratio**：选择图像方向（自由比例、横屏、竖屏、方形）
- **temperature**：控制生成多样性的参数（0.0-2.0）
- **seed** (可选)：随机种子，指定值可重现结果
- **images** (可选)：参考图像输入，支持多张图片

**输出：**
- **image**：生成的图像
- **API Respond**：API返回的文本信息

## 获取API密钥

1. 访问[Google AI Studio](https://aistudio.google.com/apikey)
2. 创建账户并生成API密钥
3. 在节点中输入API密钥

## 使用说明

- 温度值范围：0.0到2.0
- 支持多张参考图像输入
- API可能有使用限制，请查阅Google官方文档