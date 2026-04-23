#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import mimetypes
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from openai import OpenAI

_SCRIPT_DIR = Path(__file__).parent
_WORKSPACE_ROOT = _SCRIPT_DIR.parent
_ENV_PATH = _WORKSPACE_ROOT / ".env"
_ = load_dotenv(_ENV_PATH)

MODEL_ALIASES = {
    "gemini-flash": "gemini-3.1-flash-image-preview",
    "gemini-3.1-flash-image-preview": "gemini-3.1-flash-image-preview",
    "gemini-pro": "gemini-3-pro-image-preview",
    "gemini-3-pro-image-preview": "gemini-3-pro-image-preview",
    "gpt-image-2": "gpt-image-2",
}

OPENAI_IMAGE_SIZE_MAP = {
    "1K": {
        "1:1": "1024x1024",
        "4:3": "1280x960",
        "16:9": "1536x864",
        "9:16": "864x1536",
        "3:4": "960x1280",
    },
    "2K": {
        "1:1": "2048x2048",
        "4:3": "2048x1536",
        "16:9": "2048x1152",
        "9:16": "1152x2048",
        "3:4": "1536x2048",
    },
    "4K": {
        "1:1": "3840x3840",
        "4:3": "3840x2880",
        "16:9": "3840x2160",
        "9:16": "2160x3840",
        "3:4": "2880x3840",
    },
}


def _get_api_key_from_1password(
    vault: str = "dev",
    item: str = "dev-api-keys",
    field: str = "gemini_api_key",
) -> str | None:
    try:
        result = subprocess.run(
            ["op", "read", f"op://{vault}/{item}/{field}"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def _get_gemini_api_key() -> str:
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if api_key:
        return api_key
    api_key = _get_api_key_from_1password(field="gemini_api_key")
    if api_key:
        return api_key
    print(
        "Error: Gemini API key not found. Set GEMINI_API_KEY/GOOGLE_API_KEY or configure 1Password CLI.",
        file=sys.stderr,
    )
    sys.exit(1)


def _get_openai_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return api_key
    api_key = _get_api_key_from_1password(field="openai_api_key")
    if api_key:
        return api_key
    print(
        "Error: OpenAI API key not found. Set OPENAI_API_KEY or configure 1Password CLI.",
        file=sys.stderr,
    )
    sys.exit(1)


def _normalize_model_choice(choice: str) -> str:
    normalized = MODEL_ALIASES.get(choice)
    if normalized is None:
        supported = ", ".join(sorted(MODEL_ALIASES))
        raise ValueError(f"Unsupported model '{choice}'. Supported values: {supported}")
    return normalized


def _get_default_model_choice() -> str:
    configured = os.environ.get("IMAGE_GENERATION_MODEL", "gemini-flash")
    return _normalize_model_choice(configured)


def _resolve_generate_model(requested_model: str | None) -> tuple[str, str]:
    effective_choice = requested_model or _get_default_model_choice()
    normalized = _normalize_model_choice(effective_choice)
    if normalized == "gemini-3.1-flash-image-preview":
        return (
            "gemini",
            os.environ.get(
                "GEMINI_FLASH_IMAGE_MODEL",
                os.environ.get("GEMINI_IMAGE_GENERATION_MODEL", normalized),
            ),
        )
    if normalized == "gemini-3-pro-image-preview":
        return ("gemini", os.environ.get("GEMINI_PRO_IMAGE_MODEL", normalized))
    return ("openai", os.environ.get("OPENAI_IMAGE_MODEL", normalized))


def _resolve_upscale_model(requested_model: str | None) -> tuple[str, str]:
    effective_choice = requested_model or os.environ.get("IMAGE_UPSCALE_MODEL", "gemini-pro")
    normalized = _normalize_model_choice(effective_choice)
    if normalized == "gpt-image-2":
        raise ValueError("--upscale is not supported with gpt-image-2")
    if normalized == "gemini-3.1-flash-image-preview":
        return (
            "gemini",
            os.environ.get(
                "GEMINI_FLASH_IMAGE_MODEL",
                os.environ.get("GEMINI_IMAGE_GENERATION_MODEL", normalized),
            ),
        )
    return (
        "gemini",
        os.environ.get(
            "GEMINI_PRO_IMAGE_MODEL",
            os.environ.get("GEMINI_IMAGE_UPSCALE_MODEL", normalized),
        ),
    )


def _map_size_for_openai(image_size: str, aspect_ratio: str | None) -> str:
    aspect = aspect_ratio or "1:1"
    try:
        return OPENAI_IMAGE_SIZE_MAP[image_size][aspect]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported OpenAI size mapping for image_size={image_size}, aspect_ratio={aspect}"
        ) from exc


def _save_binary(path: str, data: bytes) -> None:
    with open(path, "wb") as handle:
        handle.write(data)
    print(f"Saved: {path}")


def _convert_to_jpeg(source: str, target: str) -> bool:
    result = subprocess.run(
        ["sips", "-s", "format", "jpeg", source, "--out", target],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"JPEG conversion failed: {result.stderr}", file=sys.stderr)
        return False
    return True


def _save_image_part(inline_data: object, output_path: str) -> bool:
    data = getattr(inline_data, "data", None)
    if not data:
        return False
    mime_type = getattr(inline_data, "mime_type", None) or "image/png"
    ext = mimetypes.guess_extension(mime_type) or ".png"
    if ext in {".jpg", ".jpeg"}:
        _save_binary(output_path, data)
        return True
    temp_path = f"{output_path}{ext}"
    _save_binary(temp_path, data)
    success = _convert_to_jpeg(temp_path, output_path)
    if success:
        Path(temp_path).unlink(missing_ok=True)
    return success


def _save_openai_b64_image(image_base64: str, output_path: str) -> bool:
    temp_path = f"{output_path}.png"
    with open(temp_path, "wb") as handle:
        handle.write(base64.b64decode(image_base64))
    success = _convert_to_jpeg(temp_path, output_path)
    if success:
        Path(temp_path).unlink(missing_ok=True)
        print(f"Saved: {output_path}")
    return success


def _build_output_path(output_spec: str, index: int) -> str:
    path = Path(output_spec)
    if path.suffix.lower() in {".jpg", ".jpeg"}:
        if index == 0:
            return str(path)
        return str(path.with_name(f"{path.stem}_{index}{path.suffix}"))
    return f"{output_spec}_{index}.jpg"


def _require_existing_files(image_paths: list[str]) -> None:
    for image_path in image_paths:
        if not Path(image_path).exists():
            print(f"Error: file not found: {image_path}", file=sys.stderr)
            sys.exit(1)


def _part_to_dict(part: types.Part) -> types.PartDict:
    if part.text is not None:
        return {"text": part.text}
    if part.inline_data is not None:
        return {
            "inline_data": {
                "data": part.inline_data.data,
                "mime_type": part.inline_data.mime_type,
            }
        }
    raise ValueError("Unsupported Gemini part shape for this CLI")


def _generate_gemini(
    model: str,
    prompt: str,
    image_paths: list[str] | None = None,
    output_prefix: str = "output",
    image_size: str = "1K",
    aspect_ratio: str | None = None,
) -> str | None:
    client = genai.Client(api_key=_get_gemini_api_key())
    print(f"Model: {model} | Size: {image_size}", file=sys.stderr)
    parts = [types.Part.from_text(text=prompt)]
    if image_paths:
        _require_existing_files(image_paths)
        for image_path in image_paths:
            data = Path(image_path).expanduser().read_bytes()
            mime, _mime = mimetypes.guess_type(image_path)
            parts.append(types.Part.from_bytes(data=data, mime_type=mime or "image/png"))
    if aspect_ratio:
        image_config = types.ImageConfig(image_size=image_size, aspect_ratio=aspect_ratio)
    else:
        image_config = types.ImageConfig(image_size=image_size)
    config = types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"], image_config=image_config)
    contents: types.ContentDict = {"role": "user", "parts": [_part_to_dict(part) for part in parts]}
    first_saved = None
    file_index = 0
    for chunk in client.models.generate_content_stream(model=model, contents=contents, config=config):
        candidate = chunk.candidates[0] if chunk.candidates else None
        content = candidate.content if candidate else None
        parts_out = content.parts if content and content.parts else []
        for part in parts_out:
            if part.text:
                print(part.text, end="", flush=True)
                continue
            out_path = _build_output_path(output_prefix, file_index)
            if _save_image_part(part.inline_data, out_path):
                if first_saved is None:
                    first_saved = out_path
                file_index += 1
    return first_saved


def _generate_openai(
    model: str,
    prompt: str,
    image_paths: list[str] | None = None,
    output_prefix: str = "output",
    image_size: str = "1K",
    aspect_ratio: str | None = None,
) -> str | None:
    client = OpenAI(api_key=_get_openai_api_key())
    size = _map_size_for_openai(image_size, aspect_ratio)
    print(f"Model: {model} | Size: {size}", file=sys.stderr)
    first_saved = None
    if image_paths:
        _require_existing_files(image_paths)
        if len(image_paths) != 1:
            print("Error: gpt-image-2 currently supports at most one --input image in this CLI.", file=sys.stderr)
            sys.exit(1)
        with open(image_paths[0], "rb") as image_file:
            result = client.images.edit(
                model=model,
                image=image_file,
                prompt=prompt,
                quality="high",
                output_format="png",
                extra_body={"size": size},
            )
    else:
        result = client.images.generate(
            model=model,
            prompt=prompt,
            quality="high",
            output_format="png",
            extra_body={"size": size},
        )
    for index, item in enumerate(result.data or []):
        if not item.b64_json:
            continue
        out_path = _build_output_path(output_prefix, index)
        if _save_openai_b64_image(item.b64_json, out_path) and first_saved is None:
            first_saved = out_path
    return first_saved


def generate(
    prompt: str,
    image_paths: list[str] | None = None,
    output_prefix: str = "output",
    image_size: str = "1K",
    aspect_ratio: str | None = None,
    model: str | None = None,
) -> str | None:
    provider, model_id = _resolve_generate_model(model)
    if provider == "gemini":
        return _generate_gemini(model_id, prompt, image_paths, output_prefix, image_size, aspect_ratio)
    return _generate_openai(model_id, prompt, image_paths, output_prefix, image_size, aspect_ratio)


def upscale(
    image_path: str,
    output_path: str,
    aspect_ratio: str = "16:9",
    model: str | None = None,
) -> str | None:
    if not Path(image_path).exists():
        print(f"Error: file not found: {image_path}", file=sys.stderr)
        sys.exit(1)
    provider, model_id = _resolve_upscale_model(model)
    if provider != "gemini":
        print("Error: upscale currently requires a Gemini image model.", file=sys.stderr)
        sys.exit(1)
    client = genai.Client(api_key=_get_gemini_api_key())
    print(f"Upscale model: {model_id} | {image_path} -> {output_path}", file=sys.stderr)
    image_bytes = Path(image_path).expanduser().read_bytes()
    mime, _mime = mimetypes.guess_type(image_path)
    prompt = (
        "Upscale this image to 4K resolution. Maintain all details, text, "
        "and structure exactly. Do not add or remove elements. "
        "Just increase the resolution and sharpness."
    )
    contents: types.ContentDict = {
        "role": "user",
        "parts": [
            _part_to_dict(types.Part.from_text(text=prompt)),
            _part_to_dict(types.Part.from_bytes(data=image_bytes, mime_type=mime or "image/jpeg")),
        ],
    }
    config = types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
        image_config=types.ImageConfig(aspect_ratio=aspect_ratio, image_size="4K"),
    )
    try:
        for chunk in client.models.generate_content_stream(model=model_id, contents=contents, config=config):
            candidate = chunk.candidates[0] if chunk.candidates else None
            content = candidate.content if candidate else None
            parts_out = content.parts if content and content.parts else []
            for part in parts_out:
                if _save_image_part(part.inline_data, output_path):
                    return output_path
    except Exception as exc:
        print(f"Upscale error: {exc}", file=sys.stderr)
        sys.exit(1)
    return None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate or upscale images using Gemini or GPT-Image-2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  generate_image.py -p "A serene mountain lake" -o lake.jpg
  generate_image.py -p "A serene mountain lake" -o lake.jpg -m gemini-pro
  generate_image.py -p "A serene mountain lake" -o lake.jpg -m gpt-image-2
  generate_image.py -p "Remove the watermark" -i photo.jpg -o clean.jpg
  generate_image.py -p "Wide banner" -o banner.jpg --size 4K --aspect-ratio 16:9
  generate_image.py --upscale -i small.jpg -o big.jpg
""",
    )
    parser.add_argument("--prompt", "-p", help="Text prompt (required for generate mode)")
    parser.add_argument("--input", "-i", action="append", help="Input image path (repeatable for multiple images)")
    parser.add_argument("--output", "-o", default="output", help="Output file path/prefix (default: output)")
    parser.add_argument("--size", "-s", default="1K", choices=["1K", "2K", "4K"], help="Image size for generate mode (default: 1K)")
    parser.add_argument("--aspect-ratio", "-a", choices=["1:1", "4:3", "16:9", "9:16", "3:4"], help="Aspect ratio (default: not set for generate, 16:9 for upscale)")
    parser.add_argument("--model", "-m", help="Generation model: gemini-flash / gemini-pro / gpt-image-2 or exact ids")
    parser.add_argument("--upscale", action="store_true", help="Upscale mode: enlarge input image to 4K (Gemini models only)")
    return parser


def _validate_args(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if args.model is not None:
        try:
            _normalize_model_choice(args.model)
        except ValueError as exc:
            parser.error(str(exc))
    if args.upscale and args.prompt:
        parser.error("--prompt cannot be used with --upscale")
    if args.upscale and (not args.input or len(args.input) != 1):
        parser.error("--upscale requires exactly one --input image")
    if not args.upscale and not args.prompt:
        parser.error("--prompt is required in generate mode")
    if args.upscale:
        try:
            _resolve_upscale_model(args.model)
        except ValueError as exc:
            parser.error(str(exc))


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    _validate_args(parser, args)
    if args.upscale:
        upscale(args.input[0], args.output, args.aspect_ratio or "16:9", args.model)
        return
    generate(args.prompt, args.input, args.output, args.size, args.aspect_ratio, args.model)


if __name__ == "__main__":
    main()
