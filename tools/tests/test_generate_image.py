from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

TOOLS_DIR = Path(__file__).resolve().parents[1]
MODULE_PATH = TOOLS_DIR / "generate_image.py"
SPEC = importlib.util.spec_from_file_location("generate_image", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
generate_image = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generate_image)


def _build_parser():
    return generate_image.build_parser()


def test_parser_defaults() -> None:
    parser = _build_parser()
    args = parser.parse_args(["-p", "a cat"])
    assert args.prompt == "a cat"
    assert args.model is None
    assert args.size == "1K"
    assert args.upscale is False


def test_resolve_generate_model_defaults_to_gemini_flash(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("IMAGE_GENERATION_MODEL", raising=False)
    monkeypatch.delenv("GEMINI_FLASH_IMAGE_MODEL", raising=False)
    monkeypatch.delenv("GEMINI_IMAGE_GENERATION_MODEL", raising=False)
    provider, model_id = generate_image._resolve_generate_model(None)
    assert provider == "gemini"
    assert model_id == "gemini-3.1-flash-image-preview"


def test_resolve_generate_model_supports_exact_ids(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("IMAGE_GENERATION_MODEL", raising=False)
    provider, model_id = generate_image._resolve_generate_model("gemini-3-pro-image-preview")
    assert provider == "gemini"
    assert model_id == "gemini-3-pro-image-preview"


def test_resolve_generate_model_supports_gpt_image_2(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("IMAGE_GENERATION_MODEL", raising=False)
    monkeypatch.delenv("OPENAI_IMAGE_MODEL", raising=False)
    provider, model_id = generate_image._resolve_generate_model("gpt-image-2")
    assert provider == "openai"
    assert model_id == "gpt-image-2"


def test_image_generation_model_env_overrides_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("IMAGE_GENERATION_MODEL", "gpt-image-2")
    provider, model_id = generate_image._resolve_generate_model(None)
    assert provider == "openai"
    assert model_id == "gpt-image-2"


def test_resolve_upscale_model_rejects_gpt(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("IMAGE_UPSCALE_MODEL", raising=False)
    with pytest.raises(ValueError, match="not supported"):
        generate_image._resolve_upscale_model("gpt-image-2")


@pytest.mark.parametrize(
    ("image_size", "aspect_ratio", "expected"),
    [
        ("1K", None, "1024x1024"),
        ("1K", "16:9", "1536x864"),
        ("2K", "4:3", "2048x1536"),
        ("4K", "16:9", "3840x2160"),
        ("4K", "9:16", "2160x3840"),
    ],
)
def test_map_size_for_openai(image_size: str, aspect_ratio: str | None, expected: str) -> None:
    assert generate_image._map_size_for_openai(image_size, aspect_ratio) == expected


def test_map_size_for_openai_rejects_unknown_aspect_ratio() -> None:
    with pytest.raises(ValueError, match="Unsupported OpenAI size mapping"):
        generate_image._map_size_for_openai("1K", "2:1")


def test_build_output_path_with_jpg_suffix() -> None:
    assert generate_image._build_output_path("cat.jpg", 0) == "cat.jpg"
    assert generate_image._build_output_path("cat.jpg", 1) == "cat_1.jpg"


def test_build_output_path_without_suffix() -> None:
    assert generate_image._build_output_path("cat", 0) == "cat_0.jpg"


def test_validate_args_requires_prompt_in_generate_mode() -> None:
    parser = _build_parser()
    args = parser.parse_args([])
    with pytest.raises(SystemExit):
        generate_image._validate_args(parser, args)


def test_validate_args_rejects_upscale_with_prompt() -> None:
    parser = _build_parser()
    args = parser.parse_args(["--upscale", "-i", "input.jpg", "-p", "test"])
    with pytest.raises(SystemExit):
        generate_image._validate_args(parser, args)


def test_validate_args_rejects_upscale_with_gpt() -> None:
    parser = _build_parser()
    args = parser.parse_args(["--upscale", "-i", "input.jpg", "-m", "gpt-image-2"])
    with pytest.raises(SystemExit):
        generate_image._validate_args(parser, args)


def test_validate_args_accepts_exact_model_id() -> None:
    parser = _build_parser()
    args = parser.parse_args(["-p", "test", "-m", "gemini-3.1-flash-image-preview"])
    generate_image._validate_args(parser, args)


def test_validate_args_rejects_unknown_model() -> None:
    parser = _build_parser()
    args = parser.parse_args(["-p", "test", "-m", "unknown-model"])
    with pytest.raises(SystemExit):
        generate_image._validate_args(parser, args)
