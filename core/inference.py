from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from env.config import DEFAULT_GGUF_PATH, GGUF_REPO_ID, MODEL_ID, SPEECH_MODEL_ID

# Keep local model and speech pipeline warm.
_llm: Any = None
_speech_pipeline: Any = None


def clean_generated_text(text: str) -> str:
    """Removes chat-template leftovers and normalizes generated story text."""
    # Tiny local models can echo role markers; strip obvious continuations.
    for marker in ("<|im_end|>", "<|im_start|>", "\nUser:", "\nAssistant:"):
        if marker in text:
            text = text.split(marker, 1)[0]
    text = re.sub(r"[ \t]+", " ", text)
    text = "\n".join(line.strip() for line in text.splitlines())
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def transcribe_audio(audio_path: object | None) -> tuple[str, str]:
    """Transcribes microphone commands for the radio quest."""
    global _speech_pipeline
    if not audio_path:
        return "", "No microphone command provided."
    try:
        from transformers import pipeline

        if _speech_pipeline is None:
            _speech_pipeline = pipeline(
                "automatic-speech-recognition",
                model=SPEECH_MODEL_ID,
                token=os.environ.get("HF_TOKEN"),
            )
        result = _speech_pipeline(str(audio_path))
        return str(
            result.get("text", "")
        ).strip(), f"Transcribed with {SPEECH_MODEL_ID}."
    except Exception as exc:
        return "", f"Speech transcription unavailable: {exc}"


def _resolve_gguf_path(log_lines: list[str]) -> str | None:
    """Finds a local GGUF file or downloads the configured one from the Hub."""
    # Prefer a manually downloaded GGUF path for Off the Grid judging.
    env_path = os.environ.get("TINY_QUEST_GGUF")
    for candidate in [env_path, DEFAULT_GGUF_PATH]:
        if candidate and Path(candidate).is_file():
            log_lines.append(f"Using GGUF file: {candidate}")
            return candidate
    try:
        from huggingface_hub import hf_hub_download

        log_lines.append(f"Downloading GGUF from {GGUF_REPO_ID}")
        return hf_hub_download(
            repo_id=GGUF_REPO_ID,
            filename=Path(DEFAULT_GGUF_PATH).name,
            token=os.environ.get("HF_TOKEN"),
        )
    except Exception as exc:
        log_lines.append(f"GGUF download unavailable: {exc}")
        return None


def run_quest_inference(prompt: str) -> tuple[str, str]:
    """Runs the local llama.cpp GGUF model when available."""
    global _llm
    log_lines: list[str] = []
    try:
        from llama_cpp import Llama

        if _llm is None:
            gguf_path = _resolve_gguf_path(log_lines)
            if not gguf_path:
                raise RuntimeError("No GGUF model file available.")
            _llm = Llama(
                model_path=gguf_path,
                n_ctx=4096,
                n_threads=max(2, os.cpu_count() or 2),
                verbose=False,
            )
            log_lines.append(f"Loaded local GGUF runtime for {MODEL_ID}.")
        else:
            log_lines.append("Using cached llama.cpp model.")
        result = _llm(
            prompt,
            max_tokens=420,
            temperature=0.72,
            top_p=0.9,
            stop=["\nPLAYER:", "\nUser:"],
        )
        text = str(result["choices"][0]["text"])
        log_lines.append("Local quest generation completed.")
        return clean_generated_text(text), "\n".join(log_lines)
    except Exception as exc:
        log_lines.append(f"Local GGUF inference unavailable: {exc}")
        log_lines.append("Returning deterministic radio scene fallback.")
        return _fallback_scene(prompt), "\n".join(log_lines)


def _fallback_scene(prompt: str) -> str:
    """Returns a stable game-shaped response when the local model is unavailable."""
    return (
        "=== BROADCAST ===\n"
        "Static clears. A tiny station voice says the path ahead splits under a lantern bridge. "
        "Your last command is treated as a cautious step forward.\n\n"
        "=== CHOICES ===\n"
        "A) Tune the dial toward the lantern bridge\n"
        "B) Inspect the folded map\n"
        "C) Call out to whoever is humming beyond the static\n\n"
        "=== INVENTORY ===\n"
        "Inventory: pocket radio, pencil, folded map\n\n"
        "=== DANGER ===\n"
        "Danger: medium\n\n"
        "=== RADIO CLUE ===\n"
        f"Radio clue: keep your next command short. Signal context: {prompt[:160]}"
    )
