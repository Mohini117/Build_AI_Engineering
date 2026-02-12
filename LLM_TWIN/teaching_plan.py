import json
import torch

def generate_teaching_plan(model, tokenizer, question, language):
    system_prompt = f"""
You are an experienced Indian teacher.

Your task is to CREATE A TEACHING PLAN for an educational video.

Rules:
- Do NOT directly answer the question
- Break explanation into steps
- Start with intuition or common confusion
- Use examples before definitions
- Output MUST be valid JSON
- Each step must include:
  - type (intuition, example, concept, solution)
  - narration (spoken explanation)
  - visual_hint (what appears on screen)

Language: {language}
"""

    user_prompt = f"Create a teaching plan for: {question}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=700,
            temperature=0.4,
            top_p=0.9,
            do_sample=True
        )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    try:
        start = decoded.find("{")
        teaching_plan = json.loads(decoded[start:])
    except Exception:
        teaching_plan = {
            "error": "JSON parsing failed",
            "raw_output": decoded
        }

    return teaching_plan
