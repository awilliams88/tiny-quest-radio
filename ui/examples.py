from __future__ import annotations

from html import escape
import gradio as gr

# Short commands demonstrate radio-style interaction.
EXAMPLE_COMMANDS = [
    {"label": "Inspect", "command": "Inspect the object making the ticking sound."},
    {"label": "Tune", "command": "Tune the radio toward the clearest voice."},
    {"label": "Help", "command": "Ask the station host for one clue."},
    {"label": "Brave", "command": "Step through the glowing door carefully."},
]


def _card_html(label: str, command: str) -> str:
    """Builds a compact command preset card."""
    return (
        '<div class="tq-example-copy">'
        f"<strong>{escape(label)}</strong>"
        f"<p>{escape(command)}</p>"
        "</div>"
    )


def render_examples(command_input: gr.Textbox) -> gr.Column:
    """Renders command examples and wires their buttons."""
    with gr.Column(elem_classes=["tq-examples-section"]) as section:
        gr.Markdown("## Quick Commands")
        with gr.Row(elem_classes=["tq-example-grid"]):
            for example in EXAMPLE_COMMANDS:
                with gr.Column(elem_classes=["tq-example-card"]):
                    gr.HTML(_card_html(str(example["label"]), str(example["command"])))
                    use_example = gr.Button(
                        "Use command",
                        size="sm",
                        elem_classes=["tq-example-btn"],
                    )
                    use_example.click(
                        fn=lambda command=str(example["command"]): command,
                        inputs=[],
                        outputs=[command_input],
                        queue=False,
                    )
    return section
