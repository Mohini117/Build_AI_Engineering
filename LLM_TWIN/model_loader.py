import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

BASE_MODEL_ID = "Qwen/Qwen2.5-3B-Instruct"
ADAPTER_ID = "Mohi117/qwen2.5-3b-teaching-assistant-lora"

def load_model():
    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL_ID,
        trust_remote_code=True,
        use_fast=False
    )

    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_ID,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",
        trust_remote_code=True
    )

    model = PeftModel.from_pretrained(
        base_model,
        ADAPTER_ID
    )

    model.eval()
    return model, tokenizer
