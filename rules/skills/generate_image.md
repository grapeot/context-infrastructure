# Skill: 图片生成与放大

使用 Gemini 或 GPT-Image-2 模型生成图片、编辑图片或放大图片分辨率。单文件 CLI 工具，也可作为 Python 模块 import。

## When to Use

用户说出以下意图时触发：
- "生成一张图片"、"画一张..."、"generate image"
- "把这个图片放大"、"upscale"、"提升分辨率"、"enlarge"
- "去掉水印"、"修改这张图"、"edit image"
- "用 GPT-Image-2 生成"、"用 OpenAI 画图"
- 任何需要调用图片生成能力的场景

## Prerequisites

- Gemini API Key，获取链：`GEMINI_API_KEY` env → `GOOGLE_API_KEY` env → 1Password CLI (`op://dev/dev-api-keys/gemini_api_key`)
- OpenAI API Key，获取链：`OPENAI_API_KEY` env → 1Password CLI (`op://dev/dev-api-keys/openai_api_key`)
  - 详见 [API Key 管理最佳实践](./bestpractice_api_key_management_1password_cli.md)
- Python 依赖：见 `tools/requirements.txt`（`google-genai>=1.73.1`, `openai>=1.0.0`, `python-dotenv>=1.0.0`），已装在 workspace 根 `.venv` 中

## Usage

工具路径：`tools/generate_image.py`

两种模式通过 `--upscale` flag 切换。

### 文生图（默认 Gemini Flash，1K）

```bash
python tools/generate_image.py -p "A serene mountain lake at sunset" -o lake.jpg
```

### 显式选择模型

```bash
python tools/generate_image.py -p "A cinematic mountain lake" -o lake.jpg --model gemini-pro
python tools/generate_image.py -p "A cinematic mountain lake" -o lake.jpg --model gemini-flash
python tools/generate_image.py -p "A cinematic mountain lake" -o lake.jpg --model gpt-image-2
```

### 图片编辑（图 + 文输入）

```bash
# 单图编辑
python tools/generate_image.py -p "Remove the watermark" -i photo.jpg -o clean.jpg

# 多图合成
python tools/generate_image.py -p "Combine these two styles" -i style.jpg -i content.jpg -o merged.jpg

# GPT-Image-2 单图编辑
python tools/generate_image.py -p "Make this image look like an observatory-grade photo" -i photo.jpg -o enhanced.jpg --model gpt-image-2
```

### 指定分辨率和宽高比

```bash
python tools/generate_image.py -p "Wide banner" -o banner.jpg --size 4K --aspect-ratio 16:9
```

对 GPT-Image-2 来说，CLI 会把 `1K / 2K / 4K` 和 aspect ratio 映射成实际像素尺寸。例如：

- `1K + 1:1` → `1024x1024`
- `1K + 16:9` → `1536x864`
- `4K + 16:9` → `3840x2160`

当前 GPT-Image-2 的 CLI 映射遵循实测边界：最长边不超过 3840。`6K` 不支持。

### 放大图片（Upscale）

保持内容不变，提升分辨率到 4K。

```bash
# 默认宽高比 16:9
python tools/generate_image.py --upscale -i small.jpg -o big.jpg

# 头像等正方形图片用 1:1
python tools/generate_image.py --upscale -i avatar.jpg -o avatar_hd.jpg --aspect-ratio 1:1
```

`--upscale` 当前只支持 Gemini 模型，不支持 `gpt-image-2`。

## 参数速查

| 参数 | 短写 | 说明 | 默认值 |
|------|------|------|--------|
| `--prompt` | `-p` | 生成 prompt（生成模式必需） | — |
| `--input` | `-i` | 输入图片路径（可多次使用） | — |
| `--output` | `-o` | 输出路径/前缀 | `output` |
| `--size` | `-s` | `1K` / `2K` / `4K` | `1K` |
| `--aspect-ratio` | `-a` | `1:1` / `4:3` / `16:9` / `9:16` / `3:4` | 生成不设，放大 `16:9` |
| `--model` | `-m` | `gemini-flash` / `gemini-pro` / `gpt-image-2`，也支持 exact model id | 默认 Gemini Flash |
| `--upscale` | — | 切换到放大模式 | `False` |

## 模型配置

可通过环境变量覆盖默认模型：

| 环境变量 | 默认值 | 用途 |
|----------|--------|------|
| `IMAGE_GENERATION_MODEL` | — | 统一覆盖默认生成模型选择 |
| `GEMINI_FLASH_IMAGE_MODEL` | `gemini-3.1-flash-image-preview` | Gemini Flash 生成模式 |
| `GEMINI_IMAGE_GENERATION_MODEL` | `gemini-3.1-flash-image-preview` | 旧的 Gemini Flash 兼容变量 |
| `GEMINI_PRO_IMAGE_MODEL` | `gemini-3-pro-image-preview` | Gemini Pro 生成模式 |
| `OPENAI_IMAGE_MODEL` | `gpt-image-2` | GPT-Image-2 生成模式 |
| `GEMINI_IMAGE_UPSCALE_MODEL` | `gemini-3-pro-image-preview` | 放大模式 |

## Python Import

```python
from tools.generate_image import generate, upscale

# 文生图
generate(prompt="A cat", output_prefix="cat", image_size="1K")

# GPT-Image-2 文生图
generate(prompt="A cat", output_prefix="cat", image_size="1K", model="gpt-image-2")

# 放大
upscale(image_path="small.jpg", output_path="big.jpg", aspect_ratio="1:1")
```

## 与 Slides Workflow 的关系

本工具是 workspace 级通用工具。[Slides Workflow](./workflow_presentation_slides.md) 在 <slides-repo> 内有自己的批量渲染器（`generate_slides.py`），两者独立、场景不同。本工具的代码源自该 repo 的 `gemini_generate_image.py` 和 `gemini_enlarge_image.py`，合并为单文件。
