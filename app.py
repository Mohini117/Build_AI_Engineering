import gradio as gr
from model_loader import load_model
from teaching_plan import generate_teaching_plan

# Load model once (cached by Spaces)
model, tokenizer = load_model()

def run_demo(question, language):
    if not question.strip():
        return {"error": "Please enter a question."}

    plan = generate_teaching_plan(model, tokenizer, question, language)
    return plan

with gr.Blocks(title="Nitish-Style Teaching LLM") as demo:
    gr.Markdown(
        """
        # 📘 Nitish-Style Teaching Assistant  
        **Pedagogy-aligned LLM generating video-ready teaching plans**

        - Fine-tuned using LoRA  
        - Focused on *how* to teach, not just *what* to answer  
        - Output is structured for explainable videos
        """
    )

    with gr.Row():
        question = gr.Textbox(
            label="Ask a concept",
            placeholder="Explain overfitting in deep learning",
            lines=2
        )

    language = gr.Dropdown(
        choices=["Hinglish", "English", "Hindi"],
        value="Hinglish",
        label="Language"
    )

    submit = gr.Button("Generate Teaching Plan")

    output = gr.JSON(label="Teaching Plan (Structured Output)")

    submit.click(
        fn=run_demo,
        inputs=[question, language],
        outputs=output
    )

demo.launch()
