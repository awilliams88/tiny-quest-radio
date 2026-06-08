from __future__ import annotations

# App copy shown in the Gradio header.
APP_TITLE = "Tiny Quest Radio"
APP_DESCRIPTION = "An audio-first branching adventure run by a tiny local model."

# Input limits keep game prompts compact.
PLAYER_INPUT_LIMIT = 1200
HISTORY_LIMIT = 8
MAX_TURNS = 12

# Public links shown in the Space footer.
GITHUB_URL = "https://github.com/awilliams88/tiny-quest-radio"
SPACE_URL = "https://huggingface.co/spaces/build-small-hackathon/tiny-quest-radio"

# Model metadata keeps docs, logs, and UI aligned.
MODEL_ID = "CohereLabs/tiny-aya-global"
GGUF_REPO_ID = "build-small-hackathon/tiny-quest-radio-aya-gguf"
SPEECH_MODEL_ID = "openai/whisper-small"
SPONSOR_NAME = "Cohere"
PARAMETER_COUNT = "3.35B"
DEFAULT_GGUF_PATH = "models/tiny-aya-global-q4_k_m.gguf"
