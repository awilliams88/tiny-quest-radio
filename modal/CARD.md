---
base_model: CohereLabs/tiny-aya-global
library_name: llama.cpp
pipeline_tag: text-generation
language:
- en
tags:
- gguf
- cohere
- llama-cpp
- interactive-fiction
- audio
- build-small-hackathon
---

# Tiny Quest Radio GGUF

Tiny Quest Radio GGUF is the planned local runtime model for the Tiny Quest
Radio Space. It starts from `CohereLabs/tiny-aya-global`, receives a small
app-format SFT adapter for radio adventure sections, then is merged and
quantized to GGUF for llama.cpp.

## Intended Use

- Audio-first branching adventure narration
- Compact all-ages interactive fiction
- Local/offline-friendly llama.cpp runtime

## Output Format

```text
=== BROADCAST ===
=== CHOICES ===
=== INVENTORY ===
=== DANGER ===
=== RADIO CLUE ===
```

## Training Recipe

- Base model: `CohereLabs/tiny-aya-global`
- Method: QLoRA SFT followed by merge and GGUF quantization
- Hardware: Modal NVIDIA A10G for adapter training
- Runtime: `llama-cpp-python` CPU inference from a Q4_K_M GGUF file
- Dataset: synthetic radio adventure scenes in the current production format

## Limitations

The model is for playful fiction. It can lose continuity in long sessions and
should not be treated as a factual assistant.
