#!/usr/bin/env python3
"""Standard OpenAI-compatible LLM/VLM client resolver.

Users only need to provide an OpenAI-compatible API via CLI arguments or
environment variables (works with DeepSeek, Qwen, GPT-4o, GLM, Kimi,
or a self-hosted vLLM GUI-Owl endpoint):
  - LLM_API_KEY  (or OPENAI_API_KEY)
  - LLM_BASE_URL (or OPENAI_BASE_URL)
  - LLM_MODEL    (or OPENAI_MODEL, e.g. deepseek-chat / qwen-vl-max / gpt-4o)
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class ModelConfig:
    api_key: str
    base_url: str
    model: str

    def safe_summary(self) -> str:
        host = self.base_url.split("//")[-1].split("/")[0] if self.base_url else "default"
        return f"model={self.model} host={host}"


def resolve_model_config(
    *,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ModelConfig:
    resolved_key = api_key or os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY") or ""
    resolved_base = (
        base_url
        or os.environ.get("LLM_BASE_URL")
        or os.environ.get("OPENAI_BASE_URL")
        or "https://api.openai.com/v1"
    ).rstrip("/")
    resolved_model = (
        model
        or os.environ.get("LLM_MODEL")
        or os.environ.get("OPENAI_MODEL")
        or "deepseek-v4.1-flash"
    )
    if not resolved_key:
        raise RuntimeError(
            "Missing LLM API key. Pass --api-key or set LLM_API_KEY / OPENAI_API_KEY."
        )
    return ModelConfig(api_key=resolved_key, base_url=resolved_base, model=resolved_model)


def create_openai_client(cfg: ModelConfig, timeout: float = 60.0) -> OpenAI:
    return OpenAI(api_key=cfg.api_key, base_url=cfg.base_url, timeout=timeout)
