---
title: Tiny Quest Radio
emoji: 📻
colorFrom: yellow
colorTo: green
sdk: gradio
sdk_version: 6.17.3
app_file: app.py
python_version: "3.12"
short_description: Audio-first branching adventure
pinned: false
tags:
- build-small-hackathon
- thousand-token-wood
- cohere
- off-the-grid
- llama-champion
- tiny-titan
- gguf
- audio
---

# Tiny Quest Radio

Tiny Quest Radio is an audio-first branching adventure game. The player speaks
or types short commands, and the radio responds with a compact scene, three
choices, inventory, danger level, and a clue.

## Model Plan

- Primary model: `CohereLabs/tiny-aya-global`
- Runtime: `llama-cpp-python` with a Q4_K_M GGUF file
- Speech input: `openai/whisper-small` local transcription
- Fine-tuned adapter: `build-small-hackathon/tiny-quest-radio-aya-lora`
- GGUF repo: `build-small-hackathon/tiny-quest-radio-aya-gguf`
- Training: Modal A10G QLoRA on current app-format radio scenes, then manual merge and GGUF quantization
- Parameter cap: Tiny Aya Global is 3.35B, under the 32B hackathon limit

If the local GGUF is not present, the app returns a deterministic radio scene
fallback so the UI remains testable.

## Hackathon Alignment

| Requirement | Tiny Quest Radio implementation |
|---|---|
| Gradio Space in `build-small-hackathon` | `build-small-hackathon/tiny-quest-radio` |
| Track | Thousand Token Wood |
| Sponsor focus | Cohere Tiny Aya Global with local GGUF runtime |
| Merit targets | Llama Champion, Off the Grid, Tiny Titan, Off-Brand |
| Multimodal input | Typed commands and microphone commands |
| Local runtime | `llama-cpp-python` reads a Q4_K_M GGUF file |
| Demo/social links | Add final demo video and social post links after recording |

## Links

- GitHub Repo: https://github.com/awilliams88/tiny-quest-radio
- Hugging Face Space: https://huggingface.co/spaces/build-small-hackathon/tiny-quest-radio
- Fine-tuned Adapter: https://huggingface.co/build-small-hackathon/tiny-quest-radio-aya-lora
- GGUF Model: https://huggingface.co/build-small-hackathon/tiny-quest-radio-aya-gguf
- Demo Video: pending final recording
- Social Post: pending final post

## Local Development

```bash
./run.sh setup
./run.sh app
./run.sh verify
```

Set `TINY_QUEST_GGUF=/path/to/model.gguf` to use a local GGUF file.

## Codebase

| Path | Purpose |
|---|---|
| `app.py` | Hugging Face Spaces entry point |
| `env/` | Runtime patches, model IDs, limits, links |
| `core/` | Game orchestration, speech transcription, llama.cpp inference, parsing |
| `ui/` | Radio console layout, quick commands, custom warm CSS |
| `modal/` | Modal QLoRA training job, dataset, GGUF model card |

## Training Data

The Modal dataset covers multiple genres, first turns, follow-up commands,
inventory changes, danger changes, and radio clues. The output target is the
current production section format used by the game UI.
