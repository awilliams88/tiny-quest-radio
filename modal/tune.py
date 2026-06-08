from __future__ import annotations

import os
from typing import Any

import modal

modal_any: Any = modal

# Modal app groups remote SFT and GGUF conversion prep.
app = modal_any.App("tiny-quest-radio-tuner")

# Container includes training and conversion dependencies.
image = (
    modal_any.Image.debian_slim()
    .apt_install("git", "cmake", "build-essential")
    .pip_install(
        "torch",
        "transformers>=4.45.0",
        "peft",
        "trl",
        "accelerate",
        "bitsandbytes",
        "datasets",
        "huggingface_hub",
    )
    .add_local_file(
        os.path.join(os.path.dirname(__file__), "dataset.py"),
        "/root/dataset.py",
    )
)

volume = modal_any.Volume.from_name("tiny-quest-checkpoints", create_if_missing=True)

MODEL_ID = "CohereLabs/tiny-aya-global"
ADAPTER_REPO_ID = "build-small-hackathon/tiny-quest-radio-aya-lora"
GGUF_REPO_ID = "build-small-hackathon/tiny-quest-radio-aya-gguf"


@app.function(
    image=image,
    gpu="A10G",
    timeout=10800,
    volumes={"/checkpoints": volume},
    secrets=[modal_any.Secret.from_name("huggingface-secret")],
)
def train_lora(model_card_content: str, hf_token: str | None = None):
    """Fine-tunes Tiny Aya on the current radio-game format before manual GGUF conversion."""
    # Remote-only imports are installed inside the Modal container.
    import io
    import os as remote_os

    import torch
    from datasets import Dataset
    from huggingface_hub import HfApi, login, upload_file
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from trl import SFTConfig, SFTTrainer

    from dataset import build_training_prompt, get_training_examples

    # Format the production radio sections as supervised chat examples.
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID, token=remote_os.environ.get("HF_TOKEN")
    )
    rows = []
    for item in get_training_examples():
        messages = [
            {
                "role": "user",
                "content": build_training_prompt(
                    str(item["genre"]), str(item["command"])
                ),
            },
            {"role": "assistant", "content": str(item["response"])},
        ]
        rows.append({"text": tokenizer.apply_chat_template(messages, tokenize=False)})
    dataset = Dataset.from_list(rows)
    print(f"Prepared {len(dataset)} Tiny Quest Radio conversations.")

    # QLoRA teaches section structure before merge and GGUF conversion.
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        quantization_config=bnb_config,
        device_map="auto",
        token=remote_os.environ.get("HF_TOKEN"),
    )
    model.config.pad_token_id = tokenizer.eos_token_id
    model = prepare_model_for_kbit_training(model)
    model = get_peft_model(
        model,
        LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM",
        ),
    )
    args = SFTConfig(
        output_dir="/checkpoints/tiny-quest-lora",
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        warmup_steps=8,
        max_steps=160,
        learning_rate=2e-4,
        bf16=True,
        logging_steps=5,
        save_strategy="steps",
        save_steps=40,
        save_total_limit=2,
        report_to="none",
        dataset_text_field="text",
        max_length=1536,
    )
    trainer = SFTTrainer(model=model, train_dataset=dataset, args=args)
    trainer.train()
    model.save_pretrained("/checkpoints/tiny-quest-final")
    tokenizer.save_pretrained("/checkpoints/tiny-quest-final")
    volume.commit()

    # Publish adapter/card and create the GGUF repo placeholder for manual conversion upload.
    hf_token = hf_token or remote_os.environ.get("HF_TOKEN")
    if hf_token:
        login(token=hf_token)
        model.push_to_hub(ADAPTER_REPO_ID)
        tokenizer.push_to_hub(ADAPTER_REPO_ID)
        api = HfApi(token=hf_token)
        api.create_repo(GGUF_REPO_ID, repo_type="model", exist_ok=True)
        upload_file(
            path_or_fileobj=io.BytesIO(model_card_content.encode("utf-8")),
            path_in_repo="README.md",
            repo_id=GGUF_REPO_ID,
            repo_type="model",
            commit_message="Update Tiny Quest Radio GGUF model card",
        )
    else:
        print("HF_TOKEN not set. Skipping Hub publish.")


@app.local_entrypoint()
def main():
    # Read the card dynamically so latest metadata is included.
    meta_path = os.path.join(os.path.dirname(__file__), "CARD.md")
    with open(meta_path, encoding="utf-8") as f:
        model_card = f.read()
    train_lora.remote(model_card_content=model_card)
